from unittest.mock import patch, call

from pytest import fixture

from app.src.budget_processor import BudgetProcessor
from app.src.database_manager import DatabaseManager


class BaseTestClass:
    @fixture(scope="class")
    def mock_db_manager(self):
        with patch.object(DatabaseManager, "__init__") as mock_db:
            mock_db.return_value = None
            yield mock_db

    @fixture(scope="class")
    def mock_create_notification_for_budget(self):
        with patch.object(DatabaseManager, "create_notification_for_budget") as mock:
            yield mock

    @fixture(scope="class")
    def mock_update_budget_notification_status(self):
        with patch.object(DatabaseManager, "update_budget_notification_status") as mock:
            yield mock

    @fixture(scope="class")
    def mock_update_shop_online_status(self):
        with patch.object(DatabaseManager, "update_shop_online_status") as mock:
            yield mock

    @fixture(scope="class")
    def mock_records(self):
        return [
            {"shop_id": 1, "budget_id": 1, "budget_amount": 1000, "amount_spent": 700},
            {"shop_id": 2, "budget_id": 2, "budget_amount": 2000, "amount_spent": 1800},
            {"shop_id": 3, "budget_id": 5, "budget_amount": 1500, "amount_spent": 1500},
            {"shop_id": 4, "budget_id": 6, "budget_amount": 3500, "amount_spent": 4500},
        ]

    @fixture(scope="class")
    def budget_processor(self, mock_db_manager):
        return BudgetProcessor()


class TestBudgetProcessorException(BaseTestClass):
    @fixture(scope="class")
    def process_budgets_and_notify(self, budget_processor,
                                   mock_create_notification_for_budget,
                                   mock_update_budget_notification_status,
                                   mock_update_shop_online_status, mock_logger):
        with patch.object(DatabaseManager, 'get_budgets_to_notify_and_offline') as mock_get_budgets:
            mock_get_budgets.return_value = [
                {"shop_id": 1, "budget_id": 1, "budget_amount": 1000, "amount_spent": 700},
                {"shop_id": 2, "budget_id": 2, "budget_amount": 2000, "amount_spent": 1800},
                {"shop_id": 3, "budget_id": 5, "budget_amount": 1500, "amount_spent": 1500},
                {"shop_id": 4, "budget_id": 6, "budget_amount": 3500, "amount_spent": 4500},
            ]
            mock_update_shop_online_status.side_effect = Exception("failed to update shop online status.")
            budget_processor.process_budgets_and_notify()

    def test_response(self, process_budgets_and_notify):
        assert process_budgets_and_notify is None

    def test_calls(self, mock_create_notification_for_budget,
                   mock_update_budget_notification_status,
                   mock_update_shop_online_status, mock_logger):

        calls = [call(1), call(2), call(5), call(6)]
        mock_create_notification_for_budget.assert_has_calls(calls)

        mock_update_budget_notification_status.assert_has_calls(calls)

        mock_update_shop_online_status.assert_has_calls([call(3), call(4)])

        mock_logger.assert_has_calls([call(f"Error processing budget record:"
                                           f" failed to update shop online status."),
                                      call(f"Error processing budget record:"
                                           f" failed to update shop online status.")])
