from __future__ import annotations

from bakery_management.database import get_connection, init_db


class BakeryService:
    def __init__(self, db_path: str | None = None):
        init_db(db_path)
        self.db_path = db_path

    def _connect(self):
        return get_connection(self.db_path)

    def add_product(self, name: str, category: str, price: float, stock: int, unit: str = "pcs") -> int:
        if not name.strip():
            raise ValueError("Product name cannot be empty.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")

        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO products (name, category, price, stock, unit) VALUES (?, ?, ?, ?, ?)",
                (name.strip(), category.strip(), float(price), int(stock), unit.strip() or "pcs"),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def list_products(self):
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM products ORDER BY category, name"
            ).fetchall()
            return [dict(row) for row in rows]

    def get_product(self, product_id: int):
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
            return dict(row) if row else None

    def add_customer(self, name: str, phone: str | None = None, email: str | None = None) -> int:
        if not name.strip():
            raise ValueError("Customer name cannot be empty.")

        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO customers (name, phone, email) VALUES (?, ?, ?)",
                (name.strip(), phone.strip() if phone else None, email.strip() if email else None),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def list_customers(self):
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM customers ORDER BY id").fetchall()
            return [dict(row) for row in rows]

    def create_order(self, customer_id: int, items: list[dict]):
        if not items:
            raise ValueError("Order must contain at least one item.")

        with self._connect() as conn:
            customer = conn.execute("SELECT id FROM customers WHERE id = ?", (customer_id,)).fetchone()
            if not customer:
                raise ValueError(f"Customer with id {customer_id} not found.")

            prepared_items = []
            total_amount = 0.0

            for item in items:
                product_id = int(item["product_id"])
                quantity = int(item["quantity"])

                if quantity <= 0:
                    raise ValueError("Order quantity must be greater than zero.")

                product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
                if not product:
                    raise ValueError(f"Product with id {product_id} not found.")
                if product["stock"] < quantity:
                    raise ValueError(f"Not enough stock for product '{product['name']}'. Available: {product['stock']}")

                subtotal = float(product["price"]) * quantity
                total_amount += subtotal
                prepared_items.append((product_id, quantity, subtotal))

            order_cursor = conn.execute(
                "INSERT INTO orders (customer_id, total_amount) VALUES (?, ?)",
                (customer_id, total_amount),
            )
            order_id = int(order_cursor.lastrowid)

            for product_id, quantity, subtotal in prepared_items:
                conn.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, subtotal) VALUES (?, ?, ?, ?)",
                    (order_id, product_id, quantity, subtotal),
                )
                conn.execute(
                    "UPDATE products SET stock = stock - ? WHERE id = ?",
                    (quantity, product_id),
                )

            conn.commit()
            return {"order_id": order_id, "customer_id": customer_id, "total_amount": total_amount}

    def list_orders(self):
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT o.id, o.customer_id, c.name AS customer_name, o.total_amount, o.created_at
                FROM orders o
                JOIN customers c ON c.id = o.customer_id
                ORDER BY o.id DESC
                """
            ).fetchall()
            return [dict(row) for row in rows]

    def get_dashboard_summary(self):
        with self._connect() as conn:
            product_count = conn.execute("SELECT COUNT(*) AS total FROM products").fetchone()["total"]
            total_stock_value = conn.execute(
                "SELECT COALESCE(SUM(price * stock), 0) AS total FROM products"
            ).fetchone()["total"]
            total_revenue = conn.execute(
                "SELECT COALESCE(SUM(total_amount), 0) AS total FROM orders"
            ).fetchone()["total"]
            low_stock_items = conn.execute(
                "SELECT id, name, stock FROM products WHERE stock <= 10 ORDER BY stock ASC, name ASC"
            ).fetchall()

            return {
                "product_count": product_count,
                "total_stock_value": float(total_stock_value),
                "total_revenue": float(total_revenue),
                "low_stock_items": [dict(row) for row in low_stock_items],
            }
