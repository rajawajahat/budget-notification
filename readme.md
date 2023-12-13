# Stylight Budget Notification System

Stylight Budget Notification System is an extension to the existing platform that empowers fashion retailers to manage their advertising budgets effectively. This system ensures that retailers receive timely notifications regarding their monthly expenditures on the Stylight platform. When a shop's budget reaches specific thresholds, the system takes appropriate actions, including sending notifications and temporarily setting shops offline.

## Overview

Stylight is a platform where fashion retailers advertise their products by specifying a budget representing the maximum amount they are willing to spend each month for exposure. Once this budget is exhausted, shops go _offline_, and their products are no longer advertised until the budget is replenished in the new month.

## Setting Up the Service

### Prerequisites

Before setting up the service, make sure your system has the following prerequisites installed:

- Docker
- Docker Compose
- Pip & Python 3.9 or later

### Steps

```bash
# 1. Clone the Repository and Navigate to the Root Directory:
git clone https://github.com/rajawajahat/budget-notification.git
cd budget-notification

# 2. Run Docker Compose to Set Up MySQL Server:
# Run Docker in the background to set up the MySQL server. Make sure to add the required environment variables by creating a `.env` file using `.env.example` as a reference.
docker-compose up -d

# 3. Initialize the Database:
# Run the `db.sql` script to set the database to its default state, followed by the `migration.sql` script available in the `app/database` directory.
docker exec -i [mysql_container_name] mysql -uroot -p[root_password] < db.sql
docker exec -i [mysql_container_name] mysql -uroot -p[root_password] < app/database/migration.sql

# 4. Create Python Virtual Environment:
python3 -m venv [environment_name]

# 5. Install Dependencies:
pip install -r requirements.txt

# 6. Run Tests Using Pytest:
pytest

# 7. Run the Service:
cd app
python main.py
```

## Assumptions
1. For every new budget (`a_budget_id`), a new expenses record with a unique ID (`a_expense_id`) will be created in the `t_notifications` table. This expense record is continuously being updated by some other service/functionality.


2. It's assumed that whenever the new budget record is created, its `a_notified` property will be 0, reflecting that the client has not been notified for this budget.Also, there is another functionality/service is responsible for updating the budget, and it will also reset `a_notified` to 0 whenever the client updates the budget, even if it's already been notified.

## Additional Thoughts
- As we are flagging the budget when we notify it, we will be avoiding sending duplicate notifications.


- For the condition when the client is already notified and later the budget was updated, the `a_notified` flag will be reset, and the client will again be notified if the spent amount reaches a certain threshold (i.e., 50 percent).


- The `a_created_at` column is introduced to cover the scenario if, in the future, we want to notify again and again after some time span.


## - Potential Improvements
- Logging, testing, and error handling could be improved.
- Error handling
- ORM could be used.
