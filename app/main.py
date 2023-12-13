import logging
from src.budget_processor import BudgetProcessor


def main():
    """
    Main function to check budgets, print notifications, and update the database.
    """

    try:
        budget_processor = BudgetProcessor()
        budget_processor.process_budgets_and_notify()
    except Exception as e:
        logging.error(f"Error in main function: {str(e)}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
