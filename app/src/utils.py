from datetime import datetime


def get_first_day_of_current_month() -> datetime.date:
    """
    Get the first day of the current month.

    Returns:
        datetime.date: The first day of the current month.
    """
    return datetime.now().date().replace(day=1)


def send_notification(notification: str) -> None:
    """
    Print the notification.

    Args:
        notification (str): The notification message.
    """
    print(notification)


def prepare_notification(budget_amount: float, amount_spent: float, shop_id: int, percentage_spent: float) -> str:
    """
    Prepare a notification message.

    Args:
        budget_amount (float): The budget amount.
        amount_spent (float): The amount spent.
        shop_id (int): The shop ID.
        percentage_spent (float): The percentage spent.

    Returns:
        str: The prepared notification message.
    """
    return (
        f"Notification: {datetime.now().date()} - Shop ID: {shop_id}, Budget: {budget_amount}, "
        f"Expenditure: {amount_spent} - {percentage_spent:.2f}%"
    )


def get_spent_percentage(budget_amount: float, amount_spent: float) -> float:
    """
    Calculate the percentage spent.

    Args:
        budget_amount (float): The budget amount.
        amount_spent (float): The amount spent.

    Returns:
        float: The percentage spent.
    """
    return (amount_spent / budget_amount) * 100
