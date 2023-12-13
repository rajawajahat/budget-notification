from datetime import datetime
from typing import List, Dict, Union
import os
import logging

from sqlalchemy import text, create_engine


class DatabaseManager:
    def __init__(self):
        """
        Initializes a new instance of DatabaseManager.

        This class is responsible for managing interactions with the database.
        """
        self._engine = create_engine(os.environ["DATABASE_URL"])

    def create_notification_for_budget(self, budget_id: int) -> None:
        """
        Add a notification for the specified budget ID.

        Args:
            budget_id (int): The budget ID for which to add a notification.
        """
        query = "INSERT INTO t_notifications (a_budget_id) VALUES (:budget_id);"
        with self._engine.begin() as conn:
            try:
                conn.execute(text(query).bindparams(budget_id=budget_id))
                logging.info(f"Notification created for budget ID {budget_id}")
            except Exception as e:
                logging.error(f"Error creating notification: {str(e)}")

    def get_budgets_to_notify_and_offline(self, target_month: datetime.date) -> List[Dict[str, Union[int, float]]]:
        """
        Retrieve budget records that need notification and offline status.

        Args:
            target_month (datetime.date): The target month for which to retrieve budget records.

        Returns:
            list: List of dictionaries representing budget records.
        """
        query = """
            SELECT
                tb.a_shop_id AS shop_id,
                tb.a_budget_id AS budget_id,
                tb.a_budget_amount AS budget_amount,
                te.a_amount_spent AS amount_spent
            FROM
                t_budgets tb
            JOIN t_expenses te ON tb.a_budget_id = te.a_budget_id
            WHERE
                tb.a_month = :target_month
                AND (
                    (te.a_amount_spent >= 0.5 * tb.a_budget_amount AND tb.a_notified = 0) OR
                    (te.a_amount_spent >= tb.a_budget_amount AND tb.a_notified = 1)
                );
        """
        with self._engine.begin() as conn:
            try:
                result = conn.execute(text(query).bindparams(target_month=target_month))
                records = [row._asdict() for row in result.fetchall()]
                return records
            except Exception as e:
                logging.error(f"Error fetching budgets to notify: {str(e)}")
                return []

    def update_budget_notification_status(self, budget_id: int) -> None:
        """
        Update the notification status for a specific budget.

        Args:
            budget_id (int): The ID of the budget.
        """
        query = "UPDATE t_budgets SET a_notified = 1 WHERE a_budget_id = :budget_id;"
        with self._engine.begin() as conn:
            try:
                conn.execute(text(query).bindparams(budget_id=budget_id))
                logging.info(f"Notification status updated for budget ID {budget_id}")
            except Exception as e:
                logging.error(f"Error updating notification status: {str(e)}")

    def update_shop_online_status(self, shop_id: int) -> None:
        """
        Update the online status for a specific shop.

        Args:
            shop_id (int): The ID of the shop.
        """
        query = "UPDATE t_shops SET a_online = 0 WHERE a_id = :shop_id;"
        with self._engine.begin() as conn:
            try:
                conn.execute(text(query).bindparams(shop_id=shop_id))
                logging.info(f"Online status updated for shop ID {shop_id}")
            except Exception as e:
                logging.error(f"Error updating online status: {str(e)}")
