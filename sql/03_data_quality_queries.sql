-- Total imported records
SELECT COUNT(*) AS total_client_records
FROM banking_clients;

-- Duplicate source customer identifiers
SELECT
    customer_id,
    COUNT(*) AS record_count
FROM banking_clients
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY record_count DESC, customer_id;

-- Missing-value check across important columns
SELECT
    COUNT(*) FILTER (WHERE customer_id IS NULL) AS missing_customer_id,
    COUNT(*) FILTER (WHERE joined_date IS NULL) AS missing_joined_date,
    COUNT(*) FILTER (WHERE estimated_income IS NULL) AS missing_estimated_income,
    COUNT(*) FILTER (WHERE loan_amount IS NULL) AS missing_loan_amount,
    COUNT(*) FILTER (WHERE risk_score IS NULL) AS missing_risk_score
FROM banking_clients;

-- Logical validation checks
SELECT
    COUNT(*) FILTER (WHERE age < 18 OR age > 100) AS age_requires_review,
    COUNT(*) FILTER (WHERE risk_score NOT BETWEEN 1 AND 5) AS invalid_risk_score,
    COUNT(*) FILTER (WHERE loan_amount < 0) AS negative_loan_amount,
    COUNT(*) FILTER (WHERE estimated_income < 0) AS negative_income
FROM banking_clients;