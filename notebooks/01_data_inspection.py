
"""Inspect the raw datasets for the Placement Skills Gap Analytics Dashboard."""

from pathlib import Path

import pandas as pd


def inspect_dataset(file_path: Path, dataset_name: str) -> None:
    """Display the structure and basic data-quality checks for a CSV dataset."""

    print(f"\n{'=' * 70}")
    print(f"DATASET: {dataset_name}")
    print(f"{'=' * 70}")

    # Load the original dataset without modifying its contents.
    df = pd.read_csv(file_path, low_memory=False)

    # Display the dataset dimensions and column information.
    print(f"\nShape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print("\nColumn names and data types:")
    print(df.dtypes.to_string())

    # Check missing values and duplicate records.
    print("\nMissing values by column:")
    missing = df.isnull().sum()
    print(missing[missing > 0].sort_values(ascending=False).to_string()
          if missing.any() else "No missing values found.")

    print(f"\nTotal duplicate rows: {df.duplicated().sum():,}")

    # Show sample records for understanding the data.
    print("\nFirst 5 records:")
    print(df.head().to_string())

    print("\nMemory usage: "
          f"{df.memory_usage(deep=True).sum() / (1024 ** 2):,.2f} MB")


def main() -> None:
    """Inspect both raw datasets without changing the original files."""

    # Resolve paths relative to the project root.
    project_root = Path(__file__).resolve().parent.parent
    raw_data_dir = project_root / "data" / "raw"

    datasets = {
        "India Tech Career Intelligence": (
            raw_data_dir / "indian_tech_career_intelligence_2026.csv"
        ),
        "Student Placement Prediction": (
            raw_data_dir / "student_placement_prediction_dataset_2026.csv"
        ),
    }

    # Validate paths before attempting to read the datasets.
    for name, file_path in datasets.items():
        if not file_path.is_file():
            raise FileNotFoundError(
                f"Dataset not found: {file_path}\n"
                "Check the filename in data/raw/."
            )

        inspect_dataset(file_path, name)


if __name__ == "__main__":
    main()
