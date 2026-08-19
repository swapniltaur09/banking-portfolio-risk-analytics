from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "cleaned_banking_clients.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "transformed_banking_clients.csv"
OUTPUT_DIR = PROJECT_ROOT / "python" / "outputs" / "data_transformation"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

ANALYSIS_DATE = pd.Timestamp("2026-08-17")


def create_age_group(age: float) -> str:
    """Create business-friendly age bands."""
    if pd.isna(age):
        return "Unknown"
    if age < 25:
        return "18-24"
    if age < 35:
        return "25-34"
    if age < 45:
        return "35-44"
    if age < 55:
        return "45-54"
    if age < 65:
        return "55-64"
    return "65+"


def create_risk_score_band(risk_score: float) -> str:
    """Group numeric Risk Score without assuming its business direction."""
    if pd.isna(risk_score):
        return "Unknown"
    if risk_score <= 2:
        return "Score 1-2"
    if risk_score == 3:
        return "Score 3"
    return "Score 4-5"


def create_loan_to_income_band(ratio: float) -> str:
    """Group loan exposure relative to estimated income."""
    if pd.isna(ratio):
        return "Unavailable"
    if ratio < 1:
        return "Below 1x Income"
    if ratio < 3:
        return "1x to Below 3x Income"
    return "3x+ Income"


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found. Expected file at: {INPUT_FILE}"
        )

    dataframe = pd.read_csv(INPUT_FILE, parse_dates=["joined_date"])

    # 1. Demographic and tenure columns.
    dataframe["age_group"] = dataframe["age"].apply(create_age_group)

    dataframe["customer_tenure_years"] = (
        (ANALYSIS_DATE - dataframe["joined_date"]).dt.days / 365.25
    ).round(1)

    # 2. Income segmentation based on the actual dataset quartiles.
    dataframe["income_segment"] = pd.qcut(
        dataframe["estimated_income"],
        q=4,
        labels=["Lower Income", "Lower-Middle Income", "Upper-Middle Income", "Higher Income"],
    )

    # 3. Loan segmentation based on the actual dataset quartiles.
    dataframe["loan_amount_segment"] = pd.qcut(
        dataframe["loan_amount"],
        q=4,
        labels=["Lower Loan", "Lower-Middle Loan", "Upper-Middle Loan", "Higher Loan"],
        duplicates="drop",
    )

    # 4. Risk grouping: keeps the original numeric score and avoids unsupported
    # low/medium/high risk labels until the source scoring definition is confirmed.
    dataframe["risk_score_band"] = dataframe["risk_score"].apply(
        create_risk_score_band
    )

    # 5. Exposure and balance metrics.
    dataframe["loan_to_income_ratio"] = np.where(
        dataframe["estimated_income"] > 0,
        dataframe["loan_amount"] / dataframe["estimated_income"],
        np.nan,
    ).round(2)

    dataframe["loan_to_income_band"] = dataframe["loan_to_income_ratio"].apply(
        create_loan_to_income_band
    )

    dataframe["total_account_balance"] = (
        dataframe["checking_account"]
        + dataframe["saving_account"]
        + dataframe["foreign_currency_account"]
    ).round(2)

    dataframe["total_lending_exposure"] = (
        dataframe["loan_amount"]
        + dataframe["business_lending"]
        + dataframe["credit_card_balance"]
    ).round(2)

    # 6. Count active product categories using actual positive balances/counts.
    product_conditions = [
        dataframe["credit_card_count"] > 0,
        dataframe["loan_amount"] > 0,
        dataframe["deposit_amount"] > 0,
        dataframe["checking_account"] > 0,
        dataframe["saving_account"] > 0,
        dataframe["foreign_currency_account"] > 0,
        dataframe["business_lending"] > 0,
    ]

    dataframe["active_product_category_count"] = np.select(
        product_conditions,
        [1, 1, 1, 1, 1, 1, 1],
        default=0,
    )

    dataframe["active_product_category_count"] = sum(
        condition.astype(int) for condition in product_conditions
    )

    # Save transformed dataset.
    dataframe.to_csv(OUTPUT_FILE, index=False)

    derived_columns_dictionary = pd.DataFrame(
        [
            {
                "derived_column": "age_group",
                "logic": "Age grouped into 18-24, 25-34, 35-44, 45-54, 55-64, and 65+.",
            },
            {
                "derived_column": "customer_tenure_years",
                "logic": "Years between Joined Date and 17-Aug-2026.",
            },
            {
                "derived_column": "income_segment",
                "logic": "Four income groups created from dataset quartiles.",
            },
            {
                "derived_column": "loan_amount_segment",
                "logic": "Four loan amount groups created from dataset quartiles.",
            },
            {
                "derived_column": "risk_score_band",
                "logic": "Risk Score grouped as Score 1-2, Score 3, and Score 4-5 without assuming direction.",
            },
            {
                "derived_column": "loan_to_income_ratio",
                "logic": "Loan Amount divided by Estimated Income; this is exposure-to-income, not EMI ratio.",
            },
            {
                "derived_column": "loan_to_income_band",
                "logic": "Loan-to-income ratio grouped as below 1x, 1x to below 3x, and 3x+.",
            },
            {
                "derived_column": "total_account_balance",
                "logic": "Checking Account + Saving Account + Foreign Currency Account.",
            },
            {
                "derived_column": "total_lending_exposure",
                "logic": "Loan Amount + Business Lending + Credit Card Balance.",
            },
            {
                "derived_column": "active_product_category_count",
                "logic": "Count of product categories with a positive value or card count.",
            },
        ]
    )

    derived_columns_dictionary.to_csv(
        OUTPUT_DIR / "derived_columns_dictionary.csv",
        index=False,
    )

    validation_report = pd.DataFrame(
        {
            "validation_check": [
                "Missing age groups",
                "Missing income segments",
                "Missing loan-to-income ratios",
                "Negative customer tenure years",
            ],
            "record_count": [
                dataframe["age_group"].eq("Unknown").sum(),
                dataframe["income_segment"].isna().sum(),
                dataframe["loan_to_income_ratio"].isna().sum(),
                (dataframe["customer_tenure_years"] < 0).sum(),
            ],
        }
    )

    validation_report.to_csv(
        OUTPUT_DIR / "transformation_validation_report.csv",
        index=False,
    )

    print("Data transformation completed successfully.")
    print(f"Transformed dataset saved to: {OUTPUT_FILE}")
    print(f"Derived-columns report saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()