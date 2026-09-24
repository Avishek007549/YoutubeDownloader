# Bakery Management System

A full-stack-style bakery management project built with Python and SQLite.

## Features
- Manage products and inventory
- Track customers
- Create and view sales orders
- Monitor low-stock items
- Summary dashboard for revenue and stock value
- Simple command-line interface

## Project structure

```text
Bakery-management-system/
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── bakery_management/
│   ├── __init__.py
│   ├── __main__.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── services.py
│   └── cli.py
├── data/
│   └── bakery.db
└── tests/
    └── test_bakery.py
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the app

```bash
python app.py
```

## Example commands

```bash
python app.py products add --name "Croissant" --category "Bakery" --price 3.50 --stock 25 --unit pcs
python app.py products list
python app.py customers add --name "Alice" --phone "1234567890" --email "alice@example.com"
python app.py orders add --customer-id 1 --item 1:2 --item 2:1
python app.py orders list
python app.py summary
```

## Notes
- The app uses SQLite for data storage.
- Database is created automatically in `data/bakery.db`.
- You can expand this project with a web UI or desktop interface later.
