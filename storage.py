import json
import os

PRODUCTS_FILE = "products.json"
ORDERS_FILE = "orders.json"

def load_data(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return json.load(f)
    return []

def save_data(file_name, data):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)