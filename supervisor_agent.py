from agents.order_agent import order_agent
from agents.refund_agent import refund_agent
from agents.technical_support_agent import technical_agent
from agents.product_agent import product_agent
from agents.business_agent import business_agent
from agents.customer_support_agent import customer_support_agent


def supervisor_agent(user_message):

    message = user_message.lower()

    # Refund and Return Agent
    if any(word in message for word in [
        "refund",
        "return",
        "money back",
        "exchange"
    ]):
        return refund_agent(user_message)

    # Order Agent
    if any(word in message for word in [
        "order",
        "tracking",
        "delivery",
        "shipped"
    ]):
        return order_agent(user_message)

    # Technical Support Agent
    if any(word in message for word in [
        "technical",
        "not working",
        "error",
        "wifi",
        "internet",
        "slow"
    ]):
        return technical_agent(user_message)

    # Product Recommendation Agent
    if any(word in message for word in [
        "recommend",
        "recommendation",
        "suggest",
        "laptop",
        "product",
        "buy"
    ]):
        return product_agent(user_message)

    # Business Decision Support Agent
    if any(word in message for word in [
        "business",
        "analytics",
        "kpi",
        "report",
        "workload",
        "tickets",
        "manager"
    ]):
        return business_agent(user_message)

    # General Customer Support Agent
    return customer_support_agent(user_message)