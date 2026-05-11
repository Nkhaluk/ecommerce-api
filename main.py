from fastapi import FastAPI, HTTPException, Depends

from models import Product, Order
from storage import (
    load_data,
    save_data,
    PRODUCTS_FILE,
    ORDERS_FILE
)
from auth import authenticate

app = FastAPI()

products = load_data(PRODUCTS_FILE)
orders = load_data(ORDERS_FILE)

# ------------------------
# HOME
# ------------------------

@app.get("/")
def home():
    return {"message": "E-Commerce API is running"}

# ------------------------
# PRODUCTS
# ------------------------

@app.get("/products")
def get_products():
    return products

@app.post("/products")
def create_product(product: Product):

    # Prevent duplicate IDs
    for existing_product in products:

        if existing_product["id"] == product.id:
            raise HTTPException(
                status_code=400,
                detail="Product ID already exists"
            )

    products.append(product.dict())

    save_data(PRODUCTS_FILE, products)

    return {
        "message": "Product added successfully",
        "product": product
    }

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):

    for product in products:

        if product["id"] == product_id:

            product["name"] = updated_product.name
            product["category"] = updated_product.category
            product["price"] = updated_product.price
            product["stock"] = updated_product.stock

            save_data(PRODUCTS_FILE, products)

            return {
                "message": "Product updated successfully",
                "product": product
            }

    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    for product in products:

        if product["id"] == product_id:

            products.remove(product)

            save_data(PRODUCTS_FILE, products)

            return {
                "message": "Product deleted successfully"
            }

    raise HTTPException(status_code=404, detail="Product not found")

# ------------------------
# ORDERS
# ------------------------

@app.get("/orders")
def get_orders(username: str = Depends(authenticate)):
    return {
        "logged_in_as": username,
        "orders": orders
    }

@app.post("/orders")
def create_order(order: Order):

    product_found = None

    for product in products:
        if product["id"] == order.product_id:
            product_found = product
            break

    if not product_found:
        raise HTTPException(status_code=404, detail="Product not found")

    if product_found["stock"] < order.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    total_price = product_found["price"] * order.quantity

    product_found["stock"] -= order.quantity

    order_data = order.dict()

    orders.append(order_data)

    save_data(PRODUCTS_FILE, products)
    save_data(ORDERS_FILE, orders)

    return {
        "message": "Order created successfully",
        "customer": order.customer_name,
        "product": product_found["name"],
        "quantity": order.quantity,
        "total_price": total_price
    }