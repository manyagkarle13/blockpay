import hashlib
import json
import time
from typing import List


class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float, fee: float = 0.5):
        self.sender = sender
        self.recipient = recipient
        self.amount = round(float(amount), 2)
        self.fee = fee
        self.timestamp = time.time()
        self.tx_id = self._generate_id()

    def _generate_id(self) -> str:
        raw = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def to_dict(self) -> dict:
        return {
            "tx_id": self.tx_id,
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "fee": self.fee,
            "timestamp": self.timestamp,
        }


class Block:
    def __init__(self, index: int, transactions: List[Transaction],
                 previous_hash: str, miner: str = "SYSTEM", nonce: int = 0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.miner = miner
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        data = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()

    def mine_block(self, difficulty: int) -> None:
        prefix = "0" * difficulty
        while not self.hash.startswith(prefix):
            self.nonce += 1
            self.hash = self.calculate_hash()

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "miner": self.miner,
            "nonce": self.nonce,
            "hash": self.hash,
        }

    def is_valid(self) -> bool:
        return self.hash == self.calculate_hash()


class Blockchain:
    MINING_REWARD = 10.0
    TRANSACTION_FEE = 0.5
    DIFFICULTY = 2

    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.wallets: dict = {}
        self._create_genesis_block()

    def _create_genesis_block(self):
        genesis_txs = [
            Transaction("COINBASE", "Alice", 100, fee=0),
            Transaction("COINBASE", "Bob",   50,  fee=0),
            Transaction("COINBASE", "Charlie", 30, fee=0),
        ]
        genesis = Block(0, genesis_txs, "0" * 64, miner="SYSTEM")
        genesis.mine_block(self.DIFFICULTY)
        self.chain.append(genesis)
        self.wallets = {"Alice": 100.0, "Bob": 50.0, "Charlie": 30.0}

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def get_balance(self, address: str) -> float:
        return round(self.wallets.get(address, 0.0), 2)

    def create_transaction(self, sender: str, recipient: str, amount: float) -> dict:
        if sender == recipient:
            return {"success": False, "error": "Sender and recipient must differ"}
        total = round(amount + self.TRANSACTION_FEE, 2)
        balance = self.get_balance(sender)
        if balance < total:
            return {"success": False, "error": f"Insufficient balance. Have {balance} BP, need {total} BP"}
        self.wallets[sender] = round(balance - total, 2)
        tx = Transaction(sender, recipient, amount, self.TRANSACTION_FEE)
        self.pending_transactions.append(tx)
        return {"success": True, "transaction": tx.to_dict()}

    def mine_pending_transactions(self, miner_address: str) -> dict:
        if not self.pending_transactions:
            return {"success": False, "error": "No pending transactions to mine"}
        block = Block(len(self.chain), self.pending_transactions,
                      self.last_block.hash, miner=miner_address)
        block.mine_block(self.DIFFICULTY)
        self.chain.append(block)
        total_fees = 0.0
        for tx in self.pending_transactions:
            self.wallets[tx.recipient] = round(self.wallets.get(tx.recipient, 0) + tx.amount, 2)
            total_fees += tx.fee
        self.wallets[miner_address] = round(
            self.wallets.get(miner_address, 0) + total_fees + self.MINING_REWARD, 2)
        self.pending_transactions = []
        return {"success": True, "block": block.to_dict()}

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            cur, prev = self.chain[i], self.chain[i - 1]
            if not cur.is_valid():
                return False
            if cur.previous_hash != prev.hash:
                return False
        return True

    def to_dict(self) -> dict:
        return {
            "chain": [b.to_dict() for b in self.chain],
            "length": len(self.chain),
            "pending_transactions": [tx.to_dict() for tx in self.pending_transactions],
            "wallets": self.wallets,
            "is_valid": self.is_chain_valid(),
            "difficulty": self.DIFFICULTY,
            "mining_reward": self.MINING_REWARD,
        }
