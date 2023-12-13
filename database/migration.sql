-- Step 1: Add new primary key column a_budget_id to t_budget table
ALTER TABLE t_budgets DROP PRIMARY KEY;
ALTER TABLE t_budgets ADD COLUMN a_budget_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;

-- Step 2: Add new columns to t_budgets
ALTER TABLE t_budgets ADD COLUMN a_notified BOOLEAN DEFAULT 0;
ALTER TABLE t_budgets ADD COLUMN a_last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- Step 3: Add new tables
CREATE TABLE t_expenses (
    a_expense_id  INT(11)         NOT NULL AUTO_INCREMENT,
    a_budget_id   INT(11)         NOT NULL,
    a_amount_spent DECIMAL(10,2)  NOT NULL,
    PRIMARY KEY (a_expense_id),
    FOREIGN KEY (a_budget_id) REFERENCES t_budgets (a_budget_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE t_notifications (
    a_notification_id INT(11)      NOT NULL AUTO_INCREMENT,
    a_budget_id       INT(11)      NOT NULL,
    a_created_at        TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (a_notification_id),
    FOREIGN KEY (a_budget_id) REFERENCES t_budgets (a_budget_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Step 4: Data Migration
-- Insert data into the new tables
INSERT INTO t_expenses (a_budget_id, a_amount_spent)
SELECT a_budget_id, a_amount_spent FROM t_budgets;

-- Step 5: Drop columns and tables from the old schema
ALTER TABLE t_budgets drop column a_amount_spent;
