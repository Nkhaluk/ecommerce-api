from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float
    stock: int

class Order(BaseModel):
    order_id: int
    customer_name: str
    product_id: int
    quantity: int