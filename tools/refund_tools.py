def check_return_eligibility(order_id):
    eligible_orders = ["1001", "1002"]

    if str(order_id) in eligible_orders:
        return "The order is eligible for return."

    return "The order is not eligible for return."


def check_refund_status(order_id):
    refund_status = {
        "1001": "Refund has not been initiated.",
        "1002": "Refund completed.",
        "1003": "Refund is not applicable."
    }

    return refund_status.get(
        str(order_id),
        "Refund information not found."
    )


def create_return_request(order_id):
    return f"Return request created successfully for order {order_id}."