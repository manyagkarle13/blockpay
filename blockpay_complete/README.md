# BlockPay — Blockchain Digital Payment System

Full-stack blockchain project: **Python blockchain engine** + **Django REST API** + **HTML/CSS/JS frontend**, all served from one Django server.

---

## Quick Start (3 commands)

```bash
# 1. Install
pip install -r requirements.txt

# 2. Migrate (for Django internals)
python manage.py migrate

# 3. Run
python manage.py runserver
```

Open **http://127.0.0.1:8000** → full UI loads instantly.

---

## Project Structure

```
blockpay_complete/
├── blockchain/
│   ├── blockchain.py          ← Block, Transaction, Blockchain classes (pure Python)
│   ├── views.py               ← Django views: index page + all API endpoints
│   ├── urls.py                ← URL routing (/ → frontend, /api/* → REST)
│   ├── apps.py
│   └── templates/
│       └── index.html         ← Full frontend (dark UI, 7 pages, pure HTML/CSS/JS)
├── blockpay/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt
```

---

## Pages & Features

| Page | What it does |
|---|---|
| Dashboard | Wallet balances, chain stats, pending pool, concept explainer |
| Wallets | Per-wallet balance + send/receive history |
| Send Payment | Transfer BP with live fee calculation & validation |
| Pending Pool | View all unconfirmed transactions |
| Mine Block | Run proof-of-work, select miner, see progress |
| Chain Explorer | Expand each block — hash, nonce, previous hash, transactions |
| Validate Chain | Re-compute all hashes to check for tampering |

---

## REST API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/chain/` | Full blockchain JSON |
| GET | `/api/wallets/` | All wallet balances |
| GET | `/api/balance/<name>/` | Single wallet balance |
| GET | `/api/transactions/` | Pending transactions |
| POST | `/api/transactions/` | Create transaction |
| POST | `/api/mine/` | Mine pending transactions |
| GET | `/api/validate/` | Check chain integrity |

---

## Blockchain Concepts Implemented

| Concept | Code |
|---|---|
| SHA-256 hashing | `hashlib.sha256` in `Block.calculate_hash()` |
| Proof-of-Work | `Block.mine_block(difficulty)` — nonce loop |
| Hash chain | Each block stores `previous_hash` |
| Tamper detection | `Blockchain.is_chain_valid()` |
| Transaction fee | 0.5 BP per tx → paid to miner |
| Mining reward | 10 BP per block → paid to miner |
| Pending pool | `Blockchain.pending_transactions` |
| Wallet ledger | In-memory `wallets` dict, updated per block |

---

## Cryptography Course (23IS601)

- **SHA-256**: Collision-resistant, one-way hash — used for block fingerprinting
- **Proof-of-Work**: Partial pre-image puzzle (find input → output starts with N zeros)
- **Chain integrity**: Linked hashes make tampering detectable in O(n)
- **Next step**: Add ECDSA key-pair wallets for signature-based authentication

---

*BlockPay — Built for Malnad College of Engineering, VTU Hassan · IS-A 2027*
