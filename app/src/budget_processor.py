import logging
from typing import Dict, Optional

from .database_manager import DatabaseManager
from .utils import get_first_day_of_current_month, \
    get_spent_percentage, prepare_notification, send_notification


class BudgetProcessor:

    def __init__(self):
        self._db_manager = DatabaseManager()

    def process_budgets_and_notify(self) -> None:
        """
        Process budgets for the current month and send notifications accordingly.

        Returns:
            None
        """
        month = get_first_day_of_current_month()
        budget_records = self._db_manager.get_budgets_to_notify_and_offline(month)

        for record in budget_records:
            self.process_record(record)

    def process_record(self, record: Dict[str, int]) -> None:
        """
        Process a single budget record.

        Args:
            record (dict): The budget record.
        Returns:
            None
        """
        budget_amount = record["budget_amount"]
        amount_spent = record["amount_spent"]
        shop_id = record["shop_id"]
        budget_id = record["budget_id"]

        percentage_spent = get_spent_percentage(budget_amount, amount_spent)
        notification_message = prepare_notification(budget_amount, amount_spent,
                                                    shop_id, percentage_spent)

        if amount_spent >= budget_amount:
            self._notify_and_update_database(notification_message, budget_id, shop_id)
        else:
            self._notify_and_update_database(notification_message, budget_id)

    def _notify_and_update_database(self, notification_message: str,
                                    budget_id: int, shop_id: Optional[int] = None) -> None:
        """
        Notify and update the database based on the budget status.

        Args:
            notification_message (str): The notification message.
            budget_id (int): The ID of the budget.
            shop_id (int, optional): The ID of the shop.

        Returns:
            None
        """
        send_notification(notification_message)

        try:
            self._db_manager.create_notification_for_budget(budget_id)
            self._db_manager.update_budget_notification_status(budget_id)

            if shop_id is not None:
                self._db_manager.update_shop_online_status(shop_id)
        except Exception as e:
            logging.exception(f"Error processing budget record: {str(e)}")
