
"""
Verify the processed datasets after cleaning.

Checks dataset dimensions, column names, missing values,
duplicate rows, data types, and career growth index values.
"""

from pathlib import Path
import pandas as pd


def verify_dataset(file_path: Path, dataset_name: str) -> pd.DataFrame:
    """Load a processed dataset and report its basic quality checks."""

    print("\n" + "=" * 65)
    print(f"VERIFYING: {dataset_name}")
    print("=" * 65)

    # Load the cleaned dataset.
    df = pd.read_csv(file_path)

    # Verify dimensions and column structure.
    print(f"\nDataset shape: {df.shape}")
    print(f"Number of rows: {len(df):,}")
    print(f"Number of columns: {len(df.columns)}")
    print(f"\nColumn names:\n{df.columns.tolist()}")

    # Check for missing values and exact duplicate rows.
    print(f"\nTotal missing values: {df.isnull().sum().sum()}")
    print(f"Duplicate rows: {df.duplicated().sum()}")

    # Display the data types after loading the CSV.
    print("\nColumn data types:")
    print(df.dtypes.to_string())

    return df


def main() -> None:
    """Verify both processed datasets and inspect career growth index."""

    # Locate the project root and processed datasets.
    project_root = Path(__file__).resolve().parent.parent
    processed_dir = project_root / "data" / "processed"

    industry_path = (
        processed_dir / "indian_tech_career_intelligence_cleaned.csv"
    )
    student_path = (
        processed_dir / "student_placement_prediction_cleaned.csv"
    )

    # Stop early if either processed file is missing.
    for file_path in [industry_path, student_path]:
        if not file_path.exists():
            raise FileNotFoundError(f"Processed dataset not found: {file_path}")

    # Verify both datasets.
    industry_df = verify_dataset(
        industry_path, "Industry Dataset"
    )
    student_df = verify_dataset(
        student_path, "Student Placement Dataset"
    )

    # Specifically verify career_growth_index.
    column = "career_growth_index"

    print("\n" + "=" * 65)
    print("CAREER GROWTH INDEX VERIFICATION")
    print("=" * 65)

    if column not in industry_df.columns:
        raise KeyError(f"Expected column '{column}' was not found.")

    growth = industry_df[column]

    print(f"Data type: {growth.dtype}")
    print(f"Missing values: {growth.isnull().sum()}")
    print(f"Unique values: {growth.nunique()}")
    print(f"Minimum value: {growth.min()}")
    print(f"Maximum value: {growth.max()}")
    print(f"Sample values:\n{growth.head(10).to_string(index=False)}")

    # Check whether the column is numeric.
    if pd.api.types.is_numeric_dtype(growth):
        print("\nPASS: career_growth_index is numeric.")
    else:
        print("\nFAIL: career_growth_index is not numeric.")

    # Verify the expected dimensions and excluded columns.
    expected_removed = {
        "probation_period",
        "job_description",
        "industry",
        "location_country",
        "salary_currency",
        "posted_date",
        "application_deadline",
    }

    print("\nExcluded-column verification:")
    print(f"Expected excluded columns: {len(expected_removed)}")
    print(
        "Excluded columns still present:",
        sorted(expected_removed.intersection(industry_df.columns)),
    )

    print("\nVerification completed.")


if __name__ == "__main__":
    main()
