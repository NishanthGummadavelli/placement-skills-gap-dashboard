
"""Check data quality in the original project datasets."""

from pathlib import Path

import pandas as pd


def inspect_data_quality(file_path: Path, dataset_name: str) -> None:
    """Report potential data-quality issues without modifying the dataset."""

    # Load the original CSV file.
    df = pd.read_csv(file_path, low_memory=False)

    print(f"\n{'=' * 70}")
    print(f"DATA QUALITY CHECKS: {dataset_name}")
    print(f"{'=' * 70}")

    # Check numerical ranges and summary statistics.
    numeric_columns = df.select_dtypes(include="number").columns
    print("\nNumerical summary:")
    print(df[numeric_columns].describe().round(2).to_string())

    # Identify categorical columns and inspect their distinct values.
    categorical_columns = df.select_dtypes(
        include=["object", "str", "category"]
    ).columns

    print("\nCategorical values (up to 20 per column):")
    for column in categorical_columns:
        values = df[column].dropna().unique()
        print(f"\n{column}: {len(values)} unique values")
        print(values[:20])

    # Check whether date-like columns can be parsed successfully.
    date_columns = [
        column for column in df.columns
        if "date" in column.lower() or "deadline" in column.lower()
    ]

    print("\nDate validation:")
    for column in date_columns:
        parsed_dates = pd.to_datetime(
            df[column], errors="coerce", dayfirst=True
        )
        invalid_count = (df[column].notna() & parsed_dates.isna()).sum()
        print(f"{column}: {invalid_count:,} invalid date values")

    # Check salary consistency in the industry dataset.
    if {"salary_minimum", "salary_maximum"}.issubset(df.columns):
        invalid_salary = (
            df["salary_minimum"] > df["salary_maximum"]
        ).sum()
        print(f"\nMinimum salary exceeds maximum: {invalid_salary:,}")

    # Check logical consistency in student placement records.
    if {"placement_status", "salary_package_lpa"}.issubset(df.columns):
        status = df["placement_status"].astype("string").str.strip().str.lower()
        salary = df["salary_package_lpa"]

        not_placed_with_salary = (
            status.eq("not placed") & salary.gt(0)
        ).sum()

        placed_without_salary = (
            status.eq("placed") & salary.le(0)
        ).sum()

        print("\nPlacement and salary consistency:")
        print(f"Not placed but positive salary: {not_placed_with_salary:,}")
        print(f"Placed but zero/negative salary: {placed_without_salary:,}")


def main() -> None:
    """Run quality checks on both raw datasets."""

    # Resolve paths from the project root.
    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "data" / "raw"

    datasets = {
        "India Tech Career Intelligence": (
            raw_dir / "indian_tech_career_intelligence_2026.csv"
        ),
        "Student Placement Prediction": (
            raw_dir / "student_placement_prediction_dataset_2026.csv"
        ),
    }

    # Validate file paths before starting inspection.
    for name, file_path in datasets.items():
        if not file_path.is_file():
            raise FileNotFoundError(f"Dataset not found: {file_path}")

        inspect_data_quality(file_path, name)


if __name__ == "__main__":
    main()
