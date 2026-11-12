
"""
Clean the industry and student placement datasets.

Preserves raw datasets, applies documented cleaning decisions,
and saves processed copies for exploratory data analysis.
"""

from pathlib import Path
import pandas as pd


def clean_industry_dataset(input_path: Path, output_path: Path) -> None:
    """Clean the industry dataset and save its processed copy."""

    print("\n" + "=" * 60)
    print("CLEANING INDUSTRY DATASET")
    print("=" * 60)

    # Load the original dataset without modifying the source file.
    df = pd.read_csv(input_path, low_memory=False)
    original_rows, original_columns = df.shape

    print(f"Original shape: {df.shape}")

    # Remove the seven columns excluded from our analysis.
    columns_to_remove = [
        "probation_period",
        "job_description",
        "industry",
        "location_country",
        "salary_currency",
        "posted_date",
        "application_deadline",
    ]

    # Stop if a planned column is missing, rather than silently ignoring it.
    missing_columns = [
        column for column in columns_to_remove
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Expected columns not found in industry dataset: "
            f"{missing_columns}"
        )

    df = df.drop(columns=columns_to_remove)

    # Convert percentage strings such as '85%' to numeric values such as 85.0.
    df["career_growth_index"] = pd.to_numeric(
        df["career_growth_index"]
        .astype("string")
        .str.replace("%", "", regex=False)
        .str.strip(),
        errors="raise",
    )

    # Save the cleaned dataset.
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    # Report the cleaning results.
    print(f"Original rows: {original_rows}")
    print(f"Original columns: {original_columns}")
    print(f"Cleaned shape: {df.shape}")
    print(f"Columns removed: {columns_to_remove}")
    print(f"Missing values remaining: {df.isnull().sum().sum()}")
    print(f"Duplicate rows remaining: {df.duplicated().sum()}")
    print(f"Saved to: {output_path}")


def clean_student_dataset(input_path: Path, output_path: Path) -> None:
    """Validate the student dataset and save its processed copy."""

    print("\n" + "=" * 60)
    print("CLEANING STUDENT DATASET")
    print("=" * 60)

    # Load the original student dataset.
    df = pd.read_csv(input_path, low_memory=False)
    original_shape = df.shape

    print(f"Original shape: {original_shape}")

    # Check placement status against salary without deleting any records.
    if {"placement_status", "salary_package_lpa"}.issubset(df.columns):
        status = df["placement_status"].astype("string").str.strip().str.casefold()
        salary = df["salary_package_lpa"]

        not_placed_with_salary = (
            status.eq("not placed") & salary.gt(0)
        ).sum()

        placed_without_salary = (
            status.eq("placed") & salary.le(0)
        ).sum()

        print(
            "Not Placed records with positive salary: "
            f"{not_placed_with_salary}"
        )
        print(
            "Placed records with zero/negative salary: "
            f"{placed_without_salary}"
        )

    # Preserve all student columns and rows; do not invent replacements.
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    # Report the cleaning and validation results.
    print(f"Processed shape: {df.shape}")
    print(f"Missing values remaining: {df.isnull().sum().sum()}")
    print(f"Duplicate rows remaining: {df.duplicated().sum()}")
    print(f"Saved to: {output_path}")


def main() -> None:
    """Locate project files and run both dataset-processing workflows."""

    # Resolve paths relative to the project root.
    project_root = Path(__file__).resolve().parent.parent
    raw_dir = project_root / "data" / "raw"
    processed_dir = project_root / "data" / "processed"

    industry_input = (
        raw_dir / "indian_tech_career_intelligence_2026.csv"
    )
    student_input = (
        raw_dir / "student_placement_prediction_dataset_2026.csv"
    )

    industry_output = (
        processed_dir / "indian_tech_career_intelligence_cleaned.csv"
    )
    student_output = (
        processed_dir / "student_placement_prediction_cleaned.csv"
    )

    # Verify that both raw datasets exist before starting.
    for file_path in [industry_input, student_input]:
        if not file_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {file_path}\n"
                "Check the filename and ensure the CSV is inside data/raw/."
            )

    clean_industry_dataset(industry_input, industry_output)
    clean_student_dataset(student_input, student_output)

    print("\n" + "=" * 60)
    print("DATA CLEANING COMPLETED")
    print("=" * 60)
    print(f"Processed files are stored in: {processed_dir}")


if __name__ == "__main__":
    main()
