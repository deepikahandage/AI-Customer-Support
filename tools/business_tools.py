support_data = {
    "total_tickets": 1250,
    "order_issues": 450,
    "technical_issues": 310,
    "refund_requests": 230,
    "other_issues": 260
}


def get_support_analytics():
    return support_data


def calculate_kpis():
    total = support_data["total_tickets"]

    return {
        "total_tickets": total,
        "order_issue_percentage":
            round(support_data["order_issues"] / total * 100, 2),
        "technical_issue_percentage":
            round(support_data["technical_issues"] / total * 100, 2),
        "refund_percentage":
            round(support_data["refund_requests"] / total * 100, 2)
    }


def generate_business_report():
    return {
        "summary": "Customer support analytics report",
        "data": support_data,
        "kpis": calculate_kpis()
    }