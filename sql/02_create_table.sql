CREATE TABLE IF NOT EXISTS banking_clients (
    client_record_id INTEGER PRIMARY KEY,
    customer_id VARCHAR(30),
    customer_name VARCHAR(150),
    age INTEGER CHECK (age BETWEEN 0 AND 120),
    gender VARCHAR(20),
    location_id INTEGER,
    joined_date DATE,
    banking_contact VARCHAR(150),
    nationality VARCHAR(50),
    occupation VARCHAR(150),
    investment_advisor VARCHAR(150),
    fee_structure VARCHAR(30),
    loyalty_classification VARCHAR(30),
    banking_relationship VARCHAR(50),
    estimated_income NUMERIC(18, 2),
    superannuation_savings NUMERIC(18, 2),
    credit_card_count INTEGER CHECK (credit_card_count >= 0),
    credit_card_balance NUMERIC(18, 2),
    loan_amount NUMERIC(18, 2),
    deposit_amount NUMERIC(18, 2),
    checking_account NUMERIC(18, 2),
    saving_account NUMERIC(18, 2),
    foreign_currency_account NUMERIC(18, 2),
    business_lending NUMERIC(18, 2),
    property_count INTEGER CHECK (property_count >= 0),
    risk_score INTEGER CHECK (risk_score BETWEEN 1 AND 5),
    age_group VARCHAR(20),
    customer_tenure_years NUMERIC(10, 1),
    income_segment VARCHAR(50),
    loan_amount_segment VARCHAR(50),
    risk_score_band VARCHAR(20),
    loan_to_income_ratio NUMERIC(18, 2),
    loan_to_income_band VARCHAR(50),
    total_account_balance NUMERIC(18, 2),
    total_lending_exposure NUMERIC(18, 2),
    active_product_category_count INTEGER
);

CREATE INDEX IF NOT EXISTS idx_banking_clients_risk_score
ON banking_clients (risk_score);

CREATE INDEX IF NOT EXISTS idx_banking_clients_joined_date
ON banking_clients (joined_date);

CREATE INDEX IF NOT EXISTS idx_banking_clients_relationship
ON banking_clients (banking_relationship);
