-- 1. Executive KPIs
SELECT
    COUNT(*) AS client_records,
    COUNT(DISTINCT customer_id) AS unique_source_customer_ids,
    ROUND(SUM(loan_amount), 2) AS total_loan_amount,
    ROUND(AVG(loan_amount), 2) AS average_loan_amount,
    ROUND(SUM(deposit_amount), 2) AS total_deposit_amount,
    ROUND(AVG(estimated_income), 2) AS average_estimated_income,
    ROUND(AVG(risk_score), 2) AS average_risk_score,
    ROUND(SUM(total_lending_exposure), 2) AS total_lending_exposure
FROM banking_clients;

-- 2. Risk Score distribution
SELECT
    risk_score,
    COUNT(*) AS client_records,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage_of_records,
    ROUND(AVG(estimated_income), 2) AS average_income,
    ROUND(AVG(loan_amount), 2) AS average_loan_amount
FROM banking_clients
GROUP BY risk_score
ORDER BY risk_score;

-- 3. Customer analysis by gender
SELECT
    gender,
    COUNT(*) AS client_records,
    ROUND(AVG(estimated_income), 2) AS average_income,
    ROUND(AVG(loan_amount), 2) AS average_loan_amount,
    ROUND(AVG(risk_score), 2) AS average_risk_score
FROM banking_clients
GROUP BY gender
ORDER BY client_records DESC;

-- 4. Customer analysis by age group
SELECT
    age_group,
    COUNT(*) AS client_records,
    ROUND(AVG(estimated_income), 2) AS average_income,
    ROUND(AVG(loan_amount), 2) AS average_loan_amount,
    ROUND(AVG(risk_score), 2) AS average_risk_score
FROM banking_clients
GROUP BY age_group
ORDER BY MIN(age);

-- 5. Banking relationship portfolio analysis
SELECT
    banking_relationship,
    COUNT(*) AS client_records,
    ROUND(SUM(loan_amount), 2) AS total_loan_amount,
    ROUND(SUM(total_lending_exposure), 2) AS total_lending_exposure,
    ROUND(AVG(risk_score), 2) AS average_risk_score
FROM banking_clients
GROUP BY banking_relationship
ORDER BY total_lending_exposure DESC;

-- 6. Loyalty classification analysis
SELECT
    loyalty_classification,
    COUNT(*) AS client_records,
    ROUND(SUM(deposit_amount), 2) AS total_deposit_amount,
    ROUND(SUM(loan_amount), 2) AS total_loan_amount,
    ROUND(AVG(estimated_income), 2) AS average_income
FROM banking_clients
GROUP BY loyalty_classification
ORDER BY total_loan_amount DESC;

-- 7. Income segment and loan exposure analysis
SELECT
    income_segment,
    COUNT(*) AS client_records,
    ROUND(AVG(estimated_income), 2) AS average_income,
    ROUND(AVG(loan_amount), 2) AS average_loan_amount,
    ROUND(AVG(loan_to_income_ratio), 2) AS average_loan_to_income_ratio,
    ROUND(AVG(risk_score), 2) AS average_risk_score
FROM banking_clients
GROUP BY income_segment
ORDER BY average_income;

-- 8. Customers with Score 4 or 5 for risk-review prioritization
SELECT
    client_record_id,
    customer_id,
    customer_name,
    age,
    gender,
    banking_relationship,
    estimated_income,
    loan_amount,
    loan_to_income_ratio,
    credit_card_balance,
    business_lending,
    total_lending_exposure,
    risk_score
FROM banking_clients
WHERE risk_score IN (4, 5)
ORDER BY risk_score DESC, total_lending_exposure DESC;

-- 9. Top investment-advisor portfolios by lending exposure
SELECT
    investment_advisor,
    COUNT(*) AS client_records,
    ROUND(SUM(total_lending_exposure), 2) AS total_lending_exposure,
    ROUND(AVG(risk_score), 2) AS average_risk_score
FROM banking_clients
GROUP BY investment_advisor
ORDER BY total_lending_exposure DESC
LIMIT 10;

-- 10. Customer onboarding trend
SELECT
    EXTRACT(YEAR FROM joined_date) AS joined_year,
    COUNT(*) AS client_records
FROM banking_clients
GROUP BY EXTRACT(YEAR FROM joined_date)
ORDER BY joined_year;
