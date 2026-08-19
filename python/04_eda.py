from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "transformed_banking_clients.csv"
OUTPUT_DIR = PROJECT_ROOT / "python" / "outputs" / "eda"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")

AGE_GROUP_ORDER = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
INCOME_SEGMENT_ORDER = [
    "Lower Income",
    "Lower-Middle Income",
    "Upper-Middle Income",
    "Higher Income",
]
RISK_SCORE_BAND_ORDER = ["Score 1-2", "Score 3", "Score 4-5"]


def save_chart(filename: str) -> None:
    """Save and close the active matplotlib chart."""
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close()


def create_kpi_table(dataframe: pd.DataFrame) -> None:
    """Create the core portfolio KPI table."""
    kpis = pd.DataFrame(
        {
            "KPI": [
                "Client Records",
                "Unique Source Customer IDs",
                "Total Loan Amount",
                "Average Loan Amount",
                "Total Deposit Amount",
                "Average Estimated Income",
                "Total Lending Exposure",
                "Average Account Balance",
                "Average Risk Score",
                "Average Customer Tenure (Years)",
            ],
            "Value": [
                len(dataframe),
                dataframe["customer_id"].nunique(),
                dataframe["loan_amount"].sum(),
                dataframe["loan_amount"].mean(),
                dataframe["deposit_amount"].sum(),
                dataframe["estimated_income"].mean(),
                dataframe["total_lending_exposure"].sum(),
                dataframe["total_account_balance"].mean(),
                dataframe["risk_score"].mean(),
                dataframe["customer_tenure_years"].mean(),
            ],
        }
    )

    kpis["Value"] = kpis["Value"].round(2)
    kpis.to_csv(OUTPUT_DIR / "executive_kpis.csv", index=False)


def create_analysis_tables(dataframe: pd.DataFrame) -> None:
    """Create grouped EDA tables for later SQL, insights, and Power BI work."""
    dataframe.groupby("gender").agg(
        client_records=("client_record_id", "count"),
        average_income=("estimated_income", "mean"),
        average_loan_amount=("loan_amount", "mean"),
        average_risk_score=("risk_score", "mean"),
        total_lending_exposure=("total_lending_exposure", "sum"),
    ).round(2).to_csv(OUTPUT_DIR / "gender_analysis.csv")

    dataframe.groupby("age_group", observed=False).agg(
        client_records=("client_record_id", "count"),
        average_income=("estimated_income", "mean"),
        average_loan_amount=("loan_amount", "mean"),
        average_risk_score=("risk_score", "mean"),
    ).round(2).to_csv(OUTPUT_DIR / "age_group_analysis.csv")

    dataframe.groupby("income_segment", observed=False).agg(
        client_records=("client_record_id", "count"),
        average_income=("estimated_income", "mean"),
        average_loan_amount=("loan_amount", "mean"),
        average_risk_score=("risk_score", "mean"),
        average_loan_to_income_ratio=("loan_to_income_ratio", "mean"),
    ).round(2).to_csv(OUTPUT_DIR / "income_segment_analysis.csv")

    dataframe.groupby("risk_score", observed=False).agg(
        client_records=("client_record_id", "count"),
        average_income=("estimated_income", "mean"),
        average_loan_amount=("loan_amount", "mean"),
        average_loan_to_income_ratio=("loan_to_income_ratio", "mean"),
        average_total_lending_exposure=("total_lending_exposure", "mean"),
    ).round(2).to_csv(OUTPUT_DIR / "risk_score_analysis.csv")

    dataframe.groupby("banking_relationship").agg(
        client_records=("client_record_id", "count"),
        total_loan_amount=("loan_amount", "sum"),
        average_income=("estimated_income", "mean"),
        average_risk_score=("risk_score", "mean"),
        total_lending_exposure=("total_lending_exposure", "sum"),
    ).round(2).sort_values(
        "total_loan_amount",
        ascending=False,
    ).to_csv(OUTPUT_DIR / "banking_relationship_analysis.csv")

    dataframe.groupby("loyalty_classification").agg(
        client_records=("client_record_id", "count"),
        total_loan_amount=("loan_amount", "sum"),
        total_deposit_amount=("deposit_amount", "sum"),
        average_income=("estimated_income", "mean"),
        average_risk_score=("risk_score", "mean"),
    ).round(2).sort_values(
        "total_loan_amount",
        ascending=False,
    ).to_csv(OUTPUT_DIR / "loyalty_analysis.csv")

    dataframe.groupby("investment_advisor").agg(
        client_records=("client_record_id", "count"),
        total_loan_amount=("loan_amount", "sum"),
        total_lending_exposure=("total_lending_exposure", "sum"),
        average_risk_score=("risk_score", "mean"),
    ).round(2).sort_values(
        "total_lending_exposure",
        ascending=False,
    ).to_csv(OUTPUT_DIR / "investment_advisor_analysis.csv")

    numeric_columns = [
        "age",
        "estimated_income",
        "superannuation_savings",
        "credit_card_balance",
        "loan_amount",
        "deposit_amount",
        "checking_account",
        "saving_account",
        "foreign_currency_account",
        "business_lending",
        "property_count",
        "risk_score",
        "customer_tenure_years",
        "loan_to_income_ratio",
        "total_account_balance",
        "total_lending_exposure",
        "active_product_category_count",
    ]

    dataframe[numeric_columns].corr().round(3).to_csv(
        OUTPUT_DIR / "numerical_correlation_matrix.csv"
    )


def create_charts(dataframe: pd.DataFrame) -> None:
    """Create focused, business-relevant EDA charts."""

    # 1. Customer acquisition trend.
    joined_year = dataframe["joined_date"].dt.year.value_counts().sort_index()

    plt.figure(figsize=(12, 6))
    sns.lineplot(x=joined_year.index, y=joined_year.values, marker="o")
    plt.title("Customer Records by Joined Year")
    plt.xlabel("Joined Year")
    plt.ylabel("Client Records")
    save_chart("01_customer_joined_year_trend.png")

    # 2. Age distribution.
    plt.figure(figsize=(10, 6))
    sns.histplot(data=dataframe, x="age", bins=20, kde=True, color="#1f4e79")
    plt.title("Customer Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Client Records")
    save_chart("02_age_distribution.png")

    # 3. Gender distribution.
    plt.figure(figsize=(8, 5))
    sns.countplot(data=dataframe, x="gender", hue="gender", legend=False)
    plt.title("Customer Distribution by Gender")
    plt.xlabel("Gender")
    plt.ylabel("Client Records")
    save_chart("03_gender_distribution.png")

    # 4. Banking relationship distribution.
    relationship_counts = (
        dataframe["banking_relationship"]
        .value_counts()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 6))
    sns.barplot(
        x=relationship_counts.values,
        y=relationship_counts.index,
        hue=relationship_counts.index,
        legend=False,
    )
    plt.title("Customer Distribution by Banking Relationship")
    plt.xlabel("Client Records")
    plt.ylabel("Banking Relationship")
    save_chart("04_banking_relationship_distribution.png")

    # 5. Risk Score distribution.
    plt.figure(figsize=(9, 5))
    sns.countplot(data=dataframe, x="risk_score", hue="risk_score", legend=False)
    plt.title("Risk Score Distribution")
    plt.xlabel("Risk Score")
    plt.ylabel("Client Records")
    save_chart("05_risk_score_distribution.png")

    # 6. Loan Amount distribution.
    plt.figure(figsize=(10, 6))
    sns.histplot(data=dataframe, x="loan_amount", bins=30, kde=True, color="#2e8b57")
    plt.title("Loan Amount Distribution")
    plt.xlabel("Loan Amount")
    plt.ylabel("Client Records")
    save_chart("06_loan_amount_distribution.png")

    # 7. Income by Risk Score.
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=dataframe, x="risk_score", y="estimated_income")
    plt.title("Estimated Income by Risk Score")
    plt.xlabel("Risk Score")
    plt.ylabel("Estimated Income")
    save_chart("07_income_by_risk_score.png")

    # 8. Loan Amount by Risk Score.
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=dataframe, x="risk_score", y="loan_amount")
    plt.title("Loan Amount by Risk Score")
    plt.xlabel("Risk Score")
    plt.ylabel("Loan Amount")
    save_chart("08_loan_amount_by_risk_score.png")

    # 9. Loan-to-income ratio by Risk Score.
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=dataframe, x="risk_score", y="loan_to_income_ratio")
    plt.ylim(0, dataframe["loan_to_income_ratio"].quantile(0.95))
    plt.title("Loan-to-Income Ratio by Risk Score")
    plt.xlabel("Risk Score")
    plt.ylabel("Loan-to-Income Ratio")
    save_chart("09_loan_to_income_ratio_by_risk_score.png")

    # 10. Risk score by age group.
    age_risk = (
        dataframe.groupby("age_group", observed=False)["risk_score"]
        .mean()
        .reindex(AGE_GROUP_ORDER)
        .reset_index()
    )

    plt.figure(figsize=(10, 6))
    sns.barplot(data=age_risk, x="age_group", y="risk_score", color="#c0504d")
    plt.title("Average Risk Score by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Average Risk Score")
    save_chart("10_average_risk_score_by_age_group.png")

    # 11. Loan amount by income segment.
    income_loan = (
        dataframe.groupby("income_segment", observed=False)["loan_amount"]
        .mean()
        .reindex(INCOME_SEGMENT_ORDER)
        .reset_index()
    )

    plt.figure(figsize=(11, 6))
    sns.barplot(data=income_loan, x="income_segment", y="loan_amount", color="#4f81bd")
    plt.title("Average Loan Amount by Income Segment")
    plt.xlabel("Income Segment")
    plt.ylabel("Average Loan Amount")
    plt.xticks(rotation=15)
    save_chart("11_average_loan_by_income_segment.png")

    # 12. Total lending exposure by banking relationship.
    relationship_exposure = (
        dataframe.groupby("banking_relationship")["total_lending_exposure"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=relationship_exposure,
        x="total_lending_exposure",
        y="banking_relationship",
        color="#8064a2",
    )
    plt.title("Total Lending Exposure by Banking Relationship")
    plt.xlabel("Total Lending Exposure")
    plt.ylabel("Banking Relationship")
    save_chart("12_lending_exposure_by_relationship.png")

    # 13. Correlation heatmap.
    numeric_columns = [
        "age",
        "estimated_income",
        "credit_card_balance",
        "loan_amount",
        "deposit_amount",
        "business_lending",
        "risk_score",
        "loan_to_income_ratio",
        "total_account_balance",
        "total_lending_exposure",
    ]

    correlation = dataframe[numeric_columns].corr()

    plt.figure(figsize=(13, 10))
    sns.heatmap(
        correlation,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        square=True,
    )
    plt.title("Correlation Heatmap: Banking Portfolio Variables")
    save_chart("13_correlation_heatmap.png")


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Transformed dataset not found. Expected file at: {INPUT_FILE}"
        )

    dataframe = pd.read_csv(INPUT_FILE, parse_dates=["joined_date"])

    create_kpi_table(dataframe)
    create_analysis_tables(dataframe)
    create_charts(dataframe)

    print("EDA completed successfully.")
    print(f"Charts and analysis tables saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
    