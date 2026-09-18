products = [
    {
        "name": "Laptop A",
        "price": 55000,
        "category": "Laptop",
        "use": "Programming"
    },
    {
        "name": "Laptop B",
        "price": 65000,
        "category": "Laptop",
        "use": "Programming and AI"
    },
    {
        "name": "Laptop C",
        "price": 45000,
        "category": "Laptop",
        "use": "Students"
    }
]


def search_products(category=None, max_price=None):
    results = products

    if category:
        results = [
            p for p in results
            if category.lower() in p["category"].lower()
        ]

    if max_price:
        results = [
            p for p in results
            if p["price"] <= max_price
        ]

    return results


def get_product_details(product_name):
    for product in products:
        if product["name"].lower() == product_name.lower():
            return product

    return "Product not found"


def compare_products(product1, product2):
    p1 = get_product_details(product1)
    p2 = get_product_details(product2)

    return {
        "product_1": p1,
        "product_2": p2
    }