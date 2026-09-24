import argparse

from bakery_management.services import BakeryService


def build_parser():
    parser = argparse.ArgumentParser(description="Bakery Management System")
    subparsers = parser.add_subparsers(dest="command", required=True)

    products_parser = subparsers.add_parser("products", help="Manage products")
    products_sub = products_parser.add_subparsers(dest="action", required=True)

    products_list = products_sub.add_parser("list", help="List all products")
    products_list.set_defaults(func=list_products)

    products_add = products_sub.add_parser("add", help="Add a product")
    products_add.add_argument("--name", required=True)
    products_add.add_argument("--category", required=True)
    products_add.add_argument("--price", required=True, type=float)
    products_add.add_argument("--stock", required=True, type=int)
    products_add.add_argument("--unit", default="pcs")
    products_add.set_defaults(func=add_product)

    products_low = products_sub.add_parser("low-stock", help="Show low stock products")
    products_low.set_defaults(func=low_stock_products)

    customers_parser = subparsers.add_parser("customers", help="Manage customers")
    customers_sub = customers_parser.add_subparsers(dest="action", required=True)

    customers_list = customers_sub.add_parser("list", help="List all customers")
    customers_list.set_defaults(func=list_customers)

    customers_add = customers_sub.add_parser("add", help="Add a customer")
    customers_add.add_argument("--name", required=True)
    customers_add.add_argument("--phone")
    customers_add.add_argument("--email")
    customers_add.set_defaults(func=add_customer)

    orders_parser = subparsers.add_parser("orders", help="Manage orders")
    orders_sub = orders_parser.add_subparsers(dest="action", required=True)

    orders_list = orders_sub.add_parser("list", help="List all orders")
    orders_list.set_defaults(func=list_orders)

    orders_add = orders_sub.add_parser("add", help="Create an order")
    orders_add.add_argument("--customer-id", required=True, type=int)
    orders_add.add_argument("--item", action="append", required=True, help="Format: product_id:quantity")
    orders_add.set_defaults(func=add_order)

    summary_parser = subparsers.add_parser("summary", help="Show bakery summary")
    summary_parser.set_defaults(func=show_summary)

    seed_parser = subparsers.add_parser("seed", help="Seed sample data")
    seed_parser.set_defaults(func=seed_data)

    return parser


def list_products(args):
    service = BakeryService()
    rows = service.list_products()
    if not rows:
        print("No products available.")
        return

    print("ID | Name | Category | Price | Stock | Unit")
    for row in rows:
        print(f"{row['id']} | {row['name']} | {row['category']} | ${row['price']:.2f} | {row['stock']} | {row['unit']}")


def add_product(args):
    service = BakeryService()
    product_id = service.add_product(args.name, args.category, args.price, args.stock, args.unit)
    print(f"Product added successfully with ID: {product_id}")


def low_stock_products(args):
    service = BakeryService()
    summary = service.get_dashboard_summary()
    if not summary["low_stock_items"]:
        print("No low-stock products.")
        return
    print("ID | Name | Stock")
    for item in summary["low_stock_items"]:
        print(f"{item['id']} | {item['name']} | {item['stock']}")


def list_customers(args):
    service = BakeryService()
    rows = service.list_customers()
    if not rows:
        print("No customers found.")
        return
    print("ID | Name | Phone | Email")
    for row in rows:
        print(f"{row['id']} | {row['name']} | {row['phone'] or '-'} | {row['email'] or '-'}")


def add_customer(args):
    service = BakeryService()
    customer_id = service.add_customer(args.name, args.phone, args.email)
    print(f"Customer added successfully with ID: {customer_id}")


def list_orders(args):
    service = BakeryService()
    rows = service.list_orders()
    if not rows:
        print("No orders found.")
        return
    print("ID | Customer | Total | Date")
    for row in rows:
        print(f"{row['id']} | {row['customer_name']} | ${row['total_amount']:.2f} | {row['created_at']}")


def add_order(args):
    service = BakeryService()
    parsed_items = []
    for item in args.item:
        product_id_str, quantity_str = item.split(":", 1)
        parsed_items.append({"product_id": int(product_id_str), "quantity": int(quantity_str)})

    result = service.create_order(args.customer_id, parsed_items)
    print(f"Order created successfully. Order ID: {result['order_id']}, Total: ${result['total_amount']:.2f}")


def show_summary(args):
    service = BakeryService()
    summary = service.get_dashboard_summary()
    print(f"Products: {summary['product_count']}")
    print(f"Total stock value: ${summary['total_stock_value']:.2f}")
    print(f"Total revenue: ${summary['total_revenue']:.2f}")
    print("Low stock items:")
    if not summary["low_stock_items"]:
        print("- None")
    else:
        for item in summary["low_stock_items"]:
            print(f"- {item['name']} (ID: {item['id']}): {item['stock']} left")


def seed_data(args):
    service = BakeryService()
    service.add_product("Croissant", "Bakery", 3.5, 25, "pcs")
    service.add_product("Chocolate Cake", "Desserts", 22.0, 12, "pcs")
    service.add_product("Baguette", "Bakery", 4.0, 18, "pcs")
    service.add_product("Cupcake", "Desserts", 2.75, 30, "pcs")
    service.add_customer("Alice Johnson", "1234567890", "alice@example.com")
    service.add_customer("Mark Smith", "0987654321", "mark@example.com")
    print("Sample bakery data seeded successfully.")


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
