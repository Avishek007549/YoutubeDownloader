from dataclasses import dataclass


@dataclass
class Product:
    id: int | None = None
    name: str = ""
    category: str = ""
    price: float = 0.0
    stock: int = 0
    unit: str = "pcs"


@dataclass
class Customer:
    id: int | None = None
    name: str = ""
    phone: str | None = None
    email: str | None = None


@dataclass
class OrderItem:
    product_id: int = 0
    quantity: int = 0
