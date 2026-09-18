def search_troubleshooting(issue):
    issue = issue.lower()

    if "not turning on" in issue:
        return (
            "Check the power connection, charge the device, "
            "and try restarting it."
        )

    if "internet" in issue or "wifi" in issue:
        return (
            "Restart the router, check Wi-Fi settings, "
            "and reconnect to the network."
        )

    if "slow" in issue:
        return (
            "Close unnecessary applications, restart the device, "
            "and check available storage."
        )

    return "Basic troubleshooting information is not available for this issue."


def check_warranty(product):
    return f"Warranty information checked for {product}. Please verify the purchase date."


def create_support_ticket(issue):
    return f"Technical support ticket created for: {issue}"