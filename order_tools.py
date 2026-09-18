orders = {
    "1001": {
        "status": "Shipped",
        "tracking": "TRK1001",
        "delivery": "Expected in 2 days"
    },
    "1002": {
        "status": "Delivered",
        "tracking": "TRK1002",
        "delivery": "Delivered yesterday"
    },
    "1003": {
        "status": "Processing",
        "tracking": "Not available",
        "delivery": "Expected in 4 days"
    }
}


def get_order_status(order_id):
    order = orders.get(str(order_id))

    if order:
        return order

    return {
        "error": "Order not found"
    }


def get_tracking_details(order_id):
    order = orders.get(str(order_id))

    if order:
        return order["tracking"]

    return "Order not found"


def get_delivery_date(order_id):
    order = orders.get(str(order_id))

    if order:
        return order["delivery"]

    return "Order not found"