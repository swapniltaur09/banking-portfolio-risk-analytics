from io import StringIO
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "banking_data.xlsx"
OUTPUT_DIR = PROJECT_ROOT / "python" / "outputs" / "data_understanding"
SHEET_NAME = "Clients - Banking"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")


def save_text_report(dataframe: pd.DataFrame) -> None:
    """Save dataset structure and quality checks as a text report."""
    info_buffer = StringIO()
    dataframe.info(buf=info_buffer)

    report = [
        "BANKING DATASET UNDERSTANDING REPORT",
        "=" * 60,
        f"Source file: {INPUT_FILE.name}",
        f"Sheet name: {SHEET_NAME}",
        f"Rows: {dataframe.shape[0]:,}",
        f"Columns: {dataframe.shape[1]:,}",
        "",
        "COLUMN NAMES",
        "-" * 60,
        "\n".join(dataframe.columns),
        "",
        "DATA TYPES AND NON-NULL COUNTS",
        "-" * 60,
        info_buffer.getvalue(),
        "",
        "MISSING VALUES",
        "-" * 60,
        dataframe.isna().sum().to_string(),
        "",
        "EXACT DUPLICATE ROWS",
        "-" * 60,
        str(dataframe.duplicated().sum()),
        "",
        "DUPLICATE CUSTOMER IDs",
        "-" * 60,
        str(dataframe["Customer ID"].duplicated().sum()),
        "",
        "FIRST 5 ROWS",
        "-" * 60,
        dataframe.head().to_string(index=False),
        "",
        "LAST 5 ROWS",
        "-" * 60,
        dataframe.tail().to_string(index=False),
    ]

    report_path = OUTPUT_DIR / "dataset_understanding_report.txt"
    report_path.write_text("\n".join(report), encoding="utf-8")


def save_quality_tables(dataframe: pd.DataFrame) -> None:
    """Save reusable CSV reports for missing values, uniques, and statistics."""
    missing_values = pd.DataFrame(
        {
            "Column": dataframe.columns,
            "Missing_Values": dataframe.isna().sum().values,
            "Missing_Percentage": (
                dataframe.isna().mean().mul(100).round(2).values
            ),
        }
    )
    missing_values.to_csv(OUTPUT_DIR / "missing_values_report.csv", index=False)

    unique_values = pd.DataFrame(
        {
            "Column": dataframe.columns,
            "Unique_Values": dataframe.nunique(dropna=True).values,
        }
    )
    unique_values.to_csv(OUTPUT_DIR / "unique_values_report.csv", index=False)

    numeric_columns = dataframe.select_dtypes(include="number").columns.tolist()

    if numeric_columns:
        numeric_summary = dataframe[numeric_columns].describe().T.round(2)
        numeric_summary.to_csv(OUTPUT_DIR / "numerical_summary.csv")

    duplicate_customer_ids = (
        dataframe.loc[dataframe["Customer ID"].duplicated(keep=False)]
        .sort_values("Customer ID")
    )
    duplicate_customer_ids.to_csv(
        OUTPUT_DIR / "duplicate_customer_id_records.csv",
        index=False,
    )


def create_numerical_charts(dataframe: pd.DataFrame) -> None:
    """Create histograms and box plots for numerical variables."""
    numeric_columns = dataframe.select_dtypes(include="number").columns.tolist()

    for column in numeric_columns:
        figure, axes = plt.subplots(1, 2, figsize=(13, 5))

        sns.histplot(data=dataframe, x=column, bins=30, kde=True, ax=axes[0])
        axes[0].set_title(f"{column} Distribution")

        sns.boxplot(data=dataframe, x=column, ax=axes[1])
        axes[1].set_title(f"{column} Box Plot")

        figure.tight_layout()
        figure.savefig(
            OUTPUT_DIR / f"{column.lower().replace(' ', '_')}_distribution.png",
            dpi=150,
            bbox_inches="tight",
        )
        plt.close(figure)


def create_categorical_charts(dataframe: pd.DataFrame) -> None:
    """Create readable frequency charts for categorical variables."""
    excluded_columns = {"Customer ID", "Customer Name", "Location ID"}

    categorical_columns = [
        column
        for column in dataframe.columns
        if not pd.api.types.is_numeric_dtype(dataframe[column])
        and not pd.api.types.is_datetime64_any_dtype(dataframe[column])
        and column not in excluded_columns
    ]

    for column in categorical_columns:
        frequency = dataframe[column].value_counts().head(15).sort_values()

        figure, axis = plt.subplots(figsize=(10, 6))
        sns.barplot(
            x=frequency.values,
            y=frequency.index,
            hue=frequency.index,
            palette="Blues_d",
            legend=False,
            ax=axis,
        )
        axis.set_title(f"Top Categories: {column}")
        axis.set_xlabel("Customer Records")
        axis.set_ylabel(column)

        figure.tight_layout()
        figure.savefig(
            OUTPUT_DIR / f"{column.lower().replace(' ', '_')}_frequency.png",
            dpi=150,
            bbox_inches="tight",
        )
        plt.close(figure)


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found. Expected file at: {INPUT_FILE}"
        )

    excel_file = pd.ExcelFile(INPUT_FILE)

    sheets_report = pd.DataFrame({"Sheet_Name": excel_file.sheet_names})
    sheets_report.to_csv(OUTPUT_DIR / "excel_sheet_names.csv", index=False)

    dataframe = pd.read_excel(INPUT_FILE, sheet_name=SHEET_NAME)
    dataframe.columns = dataframe.columns.str.strip()

    print("\nDataset loaded successfully.")
    print(f"Sheet: {SHEET_NAME}")
    print(f"Shape: {dataframe.shape[0]} rows x {dataframe.shape[1]} columns")

    print("\nColumn names:")
    print(dataframe.columns.tolist())

    print("\nMissing values:")
    print(dataframe.isna().sum())

    print("\nExact duplicate rows:", dataframe.duplicated().sum())
    print("Duplicate Customer IDs:", dataframe["Customer ID"].duplicated().sum())

    save_text_report(dataframe)
    save_quality_tables(dataframe)
    create_numerical_charts(dataframe)
    create_categorical_charts(dataframe)

    print(f"\nAnalysis completed successfully.")
    print(f"Reports and charts saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()