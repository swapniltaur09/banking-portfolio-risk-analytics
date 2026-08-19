from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "banking_data.xlsx"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "cleaned_banking_clients.csv"
OUTPUT_DIR = PROJECT_ROOT / "python" / "outputs" / "data_cleaning"
SHEET_NAME = "Clients - Banking"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


COLUMN_RENAME_MAP = {
    "Customer ID": "customer_id",
    "Customer Name": "customer_name",
    "Age": "age",
    "Gender": "gender",
    "Location ID": "location_id",
    "Joined Date": "joined_date",
    "Banking Contact": "banking_contact",
    "Nationality": "nationality",
    "Occupation": "occupation",
    "Investment Advisor": "investment_advisor",
    "Fee Structure": "fee_structure",
    "Loyalty Classification": "loyalty_classification",
    "Banking Relationship": "banking_relationship",
    "Estimated Income": "estimated_income",
    "Superannuation Savings": "superannuation_savings",
    "Credit Card Count": "credit_card_count",
    "Credit Card Balance": "credit_card_balance",
    "Loan Amount": "loan_amount",
    "Deposit Amount": "deposit_amount",
    "Checking Account": "checking_account",
    "Saving Account": "saving_account",
    "Foreign Currency Account": "foreign_currency_account",
    "Business Lending": "business_lending",
    "Property Count": "property_count",
    "Risk Score": "risk_score",
}

TEXT_COLUMNS = [
    "customer_id",
    "customer_name",
    "gender",
    "banking_contact",
    "nationality",
    "occupation",
    "investment_advisor",
    "fee_structure",
    "loyalty_classification",
    "banking_relationship",
]

INTEGER_COLUMNS = [
    "age",
    "location_id",
    "credit_card_count",
    "property_count",
    "risk_score",
]

FINANCIAL_COLUMNS = [
    "estimated_income",
    "superannuation_savings",
    "credit_card_balance",
    "loan_amount",
    "deposit_amount",
    "checking_account",
    "saving_account",
    "foreign_currency_account",
    "business_lending",
]


def create_outlier_report(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Identify IQR outliers for investigation without changing their values."""
    report_rows = []

    for column in FINANCIAL_COLUMNS:
        q1 = dataframe[column].quantile(0.25)
        q3 = dataframe[column].quantile(0.75)
        iqr = q3 - q1
        lower_limit = q1 - 1.5 * iqr
        upper_limit = q3 + 1.5 * iqr

        outlier_count = (
            (dataframe[column] < lower_limit)
            | (dataframe[column] > upper_limit)
        ).sum()

        report_rows.append(
            {
                "column": column,
                "q1": round(q1, 2),
                "q3": round(q3, 2),
                "iqr": round(iqr, 2),
                "lower_limit": round(lower_limit, 2),
                "upper_limit": round(upper_limit, 2),
                "outlier_count": int(outlier_count),
                "action": "Retain for business review; do not delete automatically.",
            }
        )

    return pd.DataFrame(report_rows)


def create_validation_report(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Create logical data-validation checks."""
    validation_rows = [
        {
            "validation_check": "Age outside expected range (18 to 100)",
            "invalid_record_count": int(
                ((dataframe["age"] < 18) | (dataframe["age"] > 100)).sum()
            ),
        },
        {
            "validation_check": "Risk Score outside valid range (1 to 5)",
            "invalid_record_count": int(
                ((dataframe["risk_score"] < 1) | (dataframe["risk_score"] > 5)).sum()
            ),
        },
        {
            "validation_check": "Credit Card Count less than 0",
            "invalid_record_count": int((dataframe["credit_card_count"] < 0).sum()),
        },
        {
            "validation_check": "Property Count less than 0",
            "invalid_record_count": int((dataframe["property_count"] < 0).sum()),
        },
        {
            "validation_check": "Negative financial values",
            "invalid_record_count": int(
                (dataframe[FINANCIAL_COLUMNS] < 0).any(axis=1).sum()
            ),
        },
        {
            "validation_check": "Duplicate source Customer IDs",
            "invalid_record_count": int(dataframe["customer_id"].duplicated().sum()),
        },
    ]

    return pd.DataFrame(validation_rows)


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found. Expected file at: {INPUT_FILE}"
        )

    raw_dataframe = pd.read_excel(INPUT_FILE, sheet_name=SHEET_NAME)
    rows_before_cleaning = len(raw_dataframe)

    dataframe = raw_dataframe.copy()

    # Standardize column names.
    dataframe.columns = dataframe.columns.str.strip()
    dataframe = dataframe.rename(columns=COLUMN_RENAME_MAP)

    # Keep original source ID but add a guaranteed unique record-level key.
    dataframe.insert(0, "client_record_id", range(1, len(dataframe) + 1))

    # Clean text values by removing leading and trailing spaces.
    for column in TEXT_COLUMNS:
        dataframe[column] = dataframe[column].astype("string").str.strip()

    # Correct date type.
    dataframe["joined_date"] = pd.to_datetime(
        dataframe["joined_date"],
        errors="coerce",
    )

    # Correct numerical types.
    for column in INTEGER_COLUMNS + FINANCIAL_COLUMNS:
        dataframe[column] = pd.to_numeric(dataframe[column], errors="coerce")

    # Remove only exact duplicate records. Source Customer ID duplicates are retained
    # because they contain different profile values and need business investigation.
    duplicate_rows_removed = int(dataframe.duplicated().sum())
    dataframe = dataframe.drop_duplicates().copy()

    # Store financial figures at two decimal places.
    dataframe[FINANCIAL_COLUMNS] = dataframe[FINANCIAL_COLUMNS].round(2)

    # Save quality and validation reports before exporting the cleaned dataset.
    outlier_report = create_outlier_report(dataframe)
    validation_report = create_validation_report(dataframe)

    missing_values_report = pd.DataFrame(
        {
            "column": dataframe.columns,
            "missing_values": dataframe.isna().sum().values,
            "missing_percentage": dataframe.isna().mean().mul(100).round(2).values,
        }
    )

    outlier_report.to_csv(
        OUTPUT_DIR / "outlier_investigation_report.csv",
        index=False,
    )
    validation_report.to_csv(
        OUTPUT_DIR / "data_validation_report.csv",
        index=False,
    )
    missing_values_report.to_csv(
        OUTPUT_DIR / "post_cleaning_missing_values.csv",
        index=False,
    )

    # Export the cleaned, analysis-ready dataset.
    dataframe.to_csv(OUTPUT_FILE, index=False)

    summary = [
        "DATA CLEANING SUMMARY",
        "=" * 50,
        f"Raw records: {rows_before_cleaning}",
        f"Exact duplicate rows removed: {duplicate_rows_removed}",
        f"Cleaned records: {len(dataframe)}",
        f"Cleaned columns: {len(dataframe.columns)}",
        f"Duplicate source Customer IDs retained for review: "
        f"{dataframe['customer_id'].duplicated().sum()}",
        f"Cleaned dataset saved to: {OUTPUT_FILE}",
        "",
        "Outliers were identified and retained for business review.",
        "No raw data values were overwritten or capped.",
    ]

    (OUTPUT_DIR / "cleaning_summary.txt").write_text(
        "\n".join(summary),
        encoding="utf-8",
    )

    print("Data cleaning completed successfully.")
    print(f"Cleaned dataset saved to: {OUTPUT_FILE}")
    print(f"Cleaning reports saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()