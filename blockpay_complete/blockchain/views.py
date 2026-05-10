import json
import re
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .blockchain import Blockchain

# Shared in-memory blockchain instance
_bc = Blockchain()


def get_bc():
    return _bc


# ── Frontend ──────────────────────────────────────────────────────────────────
WALLET_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _.-]{0,39}$")
WALLET_NAME_ERROR = (
    "wallet names must be 1-40 characters using letters, numbers, spaces, "
    "dots, dashes, or underscores"
)


def is_valid_wallet_name(name: str) -> bool:
    return bool(WALLET_NAME_RE.fullmatch(name))


def index(request):
    return render(request, "index.html")


# ── API ───────────────────────────────────────────────────────────────────────
@method_decorator(csrf_exempt, name="dispatch")
class ChainView(View):
    def get(self, request):
        return JsonResponse(get_bc().to_dict())


@method_decorator(csrf_exempt, name="dispatch")
class WalletsView(View):
    def get(self, request):
        bc = get_bc()
        return JsonResponse({
            "wallets": [{"address": a, "balance": b} for a, b in bc.wallets.items()]
        })


@method_decorator(csrf_exempt, name="dispatch")
class BalanceView(View):
    def get(self, request, address):
        return JsonResponse({"address": address, "balance": get_bc().get_balance(address)})


@method_decorator(csrf_exempt, name="dispatch")
class TransactionView(View):
    def get(self, request):
        bc = get_bc()
        return JsonResponse({
            "pending": [tx.to_dict() for tx in bc.pending_transactions],
            "count": len(bc.pending_transactions),
        })

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        sender = data.get("sender", "").strip()
        recipient = data.get("recipient", "").strip()
        amount = data.get("amount")
        if not sender or not recipient:
            return JsonResponse({"error": "sender and recipient are required"}, status=400)
        if not is_valid_wallet_name(sender) or not is_valid_wallet_name(recipient):
            return JsonResponse({"error": WALLET_NAME_ERROR}, status=400)
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except (TypeError, ValueError):
            return JsonResponse({"error": "amount must be a positive number"}, status=400)
        result = get_bc().create_transaction(sender, recipient, amount)
        return JsonResponse(result, status=201 if result["success"] else 400)


@method_decorator(csrf_exempt, name="dispatch")
class MineView(View):
    def post(self, request):
        try:
            data = json.loads(request.body) if request.body else {}
        except json.JSONDecodeError:
            data = {}
        miner = data.get("miner", "Alice").strip() or "Alice"
        if not is_valid_wallet_name(miner):
            return JsonResponse({"error": WALLET_NAME_ERROR}, status=400)
        result = get_bc().mine_pending_transactions(miner)
        return JsonResponse(result, status=200 if result["success"] else 400)


@method_decorator(csrf_exempt, name="dispatch")
class ValidateView(View):
    def get(self, request):
        bc = get_bc()
        valid = bc.is_chain_valid()
        return JsonResponse({
            "is_valid": valid,
            "chain_length": len(bc.chain),
            "message": "Chain is valid ✓" if valid else "Chain has been tampered with!",
        })
