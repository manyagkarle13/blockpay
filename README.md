```markdown
# BlockPay — Blockchain Digital Payment System

BlockPay is a lightweight blockchain-based digital payment platform that simulates a real cryptocurrency network. It allows users to create wallets, send payments, mine blocks, and track transactions through a clean web dashboard — all powered by a custom-built blockchain implemented in Python.

---

## Overview

BlockPay demonstrates the core mechanics of a digital currency system, including wallet management, transaction validation, Proof-of-Work mining, and chain integrity verification. The project is designed to be educational, easy to run locally, and extensible for further development.

---

## Features

- Custom blockchain engine with Proof-of-Work mining and configurable difficulty
- Wallet creation and management with unique balances per user
- Peer-to-peer style payment transfers between wallets with backend validation
- Pending transaction pool (mempool) that holds transactions until mined
- Live dashboard displaying circulation, block count, difficulty, and block rewards
- Built-in chain validator to verify blockchain consistency
- Clean, responsive web interface for seamless interaction

---

## Tech Stack

| Layer      | Technology             |
|------------|------------------------|
| Backend    | Python, Flask          |
| Database   | SQLite                 |
| Frontend   | HTML, CSS, JavaScript  |
| Blockchain | Custom Python module   |

---

## Project Structure

```
blockpay_complete/
├── blockchain/          # Core blockchain logic (blocks, chain, mining)
├── blockpay/            # Flask app (routes, views, templates)
├── db.sqlite3           # Local SQLite database
├── manage.py            # CLI entry point (run, check, migrate)
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Installation

1. Clone the repository

   ```bash
   git clone https://github.com/manyagkarle13/blockpay.git
   cd blockpay
   ```

2. Create and activate a virtual environment

   ```bash
   python -m venv venv
   ```

   On Windows:
   ```bash
   venv\Scripts\activate
   ```

   On macOS or Linux:
   ```bash
   source venv/bin/activate
   ```

3. Install the required dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application

   ```bash
   python manage.py runserver
   ```

5. Open the application in your browser

   ```
   http://127.0.0.1:8000/
   ```

---

## Usage

1. Navigate to the **Wallets** section to create one or more wallets. Each wallet starts with a default balance.
2. Use the **Send Payment** screen to transfer BlockPay coins (BP) between wallets. You can either select an existing wallet or create a new one directly from the recipient dropdown.
3. The transaction enters the **Pending Pool** and waits until a miner confirms it.
4. Once mined, a new block is appended to the chain and wallet balances are updated automatically.
5. The **Dashboard** reflects total coins in circulation, chain length, current difficulty, and block rewards in real time.

---

## Verifying the Blockchain

Check the integrity of the blockchain at any time:

```bash
python manage.py check
```

Compile all blockchain modules:

```bash
python -m compileall ./blockchain
```

---

## Validation Rules

- Wallet names may contain letters, numbers, spaces, periods, hyphens, and underscores (maximum 40 characters)
- The sender must have sufficient balance to complete a transaction
- Self-transfers (sending to the same wallet) are not permitted
- Every block is cryptographically linked to its predecessor through hashing

---

## Roadmap

- Multi-node networking and peer synchronization
- Public and private key based wallet authentication
- Transaction history export in CSV and JSON formats
- REST API documentation using OpenAPI
- Docker containerization for easier deployment

---

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a feature branch

   ```bash
   git checkout -b feature/your-feature
   ```

3. Commit your changes

   ```bash
   git commit -m "Add your feature"
   ```

4. Push to your branch

   ```bash
   git push origin feature/your-feature
   ```

5. Open a Pull Request describing your changes

---

## Author

**Manya Gkarle**
GitHub: [https://github.com/manyagkarle13](https://github.com/manyagkarle13)

---

## Acknowledgements

This project was built as an educational exploration of blockchain fundamentals, distributed ledgers, and digital payment systems. Inspired by the design principles of Bitcoin and modern fintech platforms.
```

To add it to your repo, open `README.md` in VS Code, paste the content above, save, and run:

```bash
git add README.md
git commit -m "docs: add professional README"
git push origin main
```
