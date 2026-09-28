# Banking Portfolio and Risk Analytics — KPI Framework

## KPI Rules

- The dataset contains 3,000 client records.
- `Customer ID` is not fully unique; 2,940 unique source customer IDs exist.
- `Risk Score` is recorded from 1 to 5.
- Score direction is not documented in the source data. Therefore, records with Score 4 and Score 5 are labelled as **Risk Review Records**, not automatically as “High Risk”.
- Default Rate, EMI Ratio, Credit Score, and Payment Performance KPIs are not available because those source fields do not exist.

## Executive KPIs

| KPI | Definition | Actual Baseline Value |
|---|---|---:|
| Client Records | Count of all rows using `client_record_id` | 3,000 |
| Unique Source Customer IDs | Distinct count of `customer_id` | 2,940 |
| Total Loan Amount | Sum of `loan_amount` | 1,774,158,465.76 |
| Average Loan Amount | Average of `loan_amount` | 591,386.16 |
| Total Deposit Amount | Sum of `deposit_amount` | 2,014,680,581.53 |
| Average Estimated Income | Average of `estimated_income` | 171,305.03 |
| Total Lending Exposure | Sum of `total_lending_exposure` | 4,383,966,510.63 |
| Average Account Balance | Average of `total_account_balance` | 583,884.83 |
| Average Risk Score | Average of `risk_score` | 2.25 |
| Average Customer Tenure | Average of `customer_tenure_years` | 20.6 years |

## Risk Review KPIs

| KPI | Definition | Actual Baseline Value |
|---|---|---:|
| Score 4–5 Risk Review Records | Count where `risk_score` is 4 or 5 | 482 |
| Score 4–5 Risk Review Percentage | Score 4–5 records ÷ all client records | 16.07% |
| Average Loan-to-Income Ratio | Average of `loan_to_income_ratio` | 4.72 |
| Risk Score Distribution | Count of client records by `risk_score` | Available |
| Risk Score by Demographics | Average risk score by age, gender, relationship, income group | Available |

## Customer and Portfolio KPIs

| KPI | Definition | Dashboard Page |
|---|---|---|
| Gender Distribution | Count of client records by gender | Customer Analysis |
| Age Group Distribution | Count by `age_group` | Customer Analysis |
| Income Segment Distribution | Count by `income_segment` | Customer Analysis |
| Loyalty Classification Distribution | Count by loyalty tier | Customer Analysis |
| Banking Relationship Distribution | Count by banking relationship | Executive Summary |
| Loan Amount by Relationship | Sum of loan amount by relationship | Executive Summary |
| Deposit Amount by Loyalty Tier | Sum of deposits by loyalty tier | Customer Analysis |
| Product Category Count | Average of `active_product_category_count` | Customer Analysis |
| Advisor Lending Exposure | Sum of lending exposure by advisor | Insights Dashboard |
| Customer Onboarding Trend | Count by joined year | Executive Summary |

## Unavailable KPIs

| KPI | Reason |
|---|---|
| Default Rate | Default flag/status does not exist. |
| Default Count | Default flag/status does not exist. |
| EMI Ratio | EMI amount does not exist. |
| Credit Score | Credit score field does not exist. |
| Payment Success Rate | Payment history and repayment data do not exist. |
| City-wise KPIs | Location ID exists, but city name is unavailable. |
| Loan Status KPIs | Loan status and loan ID are unavailable. |

## Dashboard KPI Card Priorities

### Executive Summary

1. Client Records
2. Total Loan Amount
3. Total Deposit Amount
4. Total Lending Exposure
5. Average Estimated Income
6. Average Risk Score
7. Score 4–5 Risk Review Percentage

### Customer Analysis

1. Unique Source Customer IDs
2. Average Customer Tenure
3. Average Account Balance
4. Average Active Product Categories
5. Average Loan Amount

### Risk Analysis

1. Score 4–5 Risk Review Records
2. Score 4–5 Risk Review Percentage
3. Average Risk Score
4. Average Loan-to-Income Ratio
5. Total Lending Exposure for Score 4–5 Records
