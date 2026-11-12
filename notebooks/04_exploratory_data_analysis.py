
"""
Exploratory Data Analysis for the Placement Skills Gap Analytics Dashboard.

Analyzes student placement outcomes and saves visualizations
for the project report and dashboard preparation.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def analyze_placement_distribution(
    df: pd.DataFrame,
    reports_dir: Path,
) -> None:
    """Summarize placement outcomes and save a distribution chart."""

    # Count students in each placement category.
    placement_counts = df["placement_status"].value_counts()
    total_students = len(df)

    # Calculate the percentage for each category.
    placement_percentages = (
        placement_counts / total_students * 100
    ).round(2)

    print("\n" + "=" * 60)
    print("STUDENT PLACEMENT DISTRIBUTION")
    print("=" * 60)
    print(f"Total students: {total_students:,}")
    print("\nPlacement counts:")
    print(placement_counts.to_string())
    print("\nPlacement percentages:")
    print(placement_percentages.to_string())

    # Create the output directory if it does not exist.
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Create and save the count chart.
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(8, 5))

    ax = sns.countplot(
        data=df,
        x="placement_status",
        hue="placement_status",
        order=placement_counts.index,
        legend=False,
    )

    ax.set_title("Student Placement Distribution")
    ax.set_xlabel("Placement Status")
    ax.set_ylabel("Number of Students")

    # Label each bar with its student count.
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f")

    plt.tight_layout()
    chart_path = reports_dir / "placement_distribution.png"
    plt.savefig(chart_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"\nChart saved to: {chart_path}")


def analyze_cgpa_vs_placement(
    df: pd.DataFrame,
    reports_dir: Path,
) -> None:
    """Compare CGPA distributions across placement categories."""

    print("\n" + "=" * 60)
    print("CGPA VS PLACEMENT STATUS")
    print("=" * 60)

    # Summarize CGPA for each placement category.
    summary = df.groupby("placement_status")["cgpa"].agg(
        ["count", "mean", "median", "min", "max"]
    )

    print("\nCGPA summary by placement status:")
    print(summary.round(2).to_string())

    # Create a box plot to compare the two groups.
    plt.figure(figsize=(8, 5))

    sns.boxplot(
        data=df,
        x="placement_status",
        y="cgpa",
        hue="placement_status",
        legend=False,
    )

    plt.title("CGPA Distribution by Placement Status")
    plt.xlabel("Placement Status")
    plt.ylabel("CGPA")
    plt.tight_layout()

    # Save the visualization for our project report.
    chart_path = reports_dir / "cgpa_vs_placement.png"
    plt.savefig(chart_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"\nChart saved to: {chart_path}")


def analyze_coding_skills_vs_placement(
    df: pd.DataFrame,
    reports_dir: Path,
) -> None:
    """Compare coding skill scores across placement categories."""

    print("\n" + "=" * 60)
    print("CODING SKILL SCORE VS PLACEMENT STATUS")
    print("=" * 60)

    # Calculate summary statistics for each placement group.
    summary = df.groupby("placement_status")[
        "coding_skill_score"
    ].agg(["count", "mean", "median", "min", "max"])

    print("\nCoding skill score summary:")
    print(summary.round(2).to_string())

    # Compare the score distributions visually.
    plt.figure(figsize=(8, 5))

    sns.boxplot(
        data=df,
        x="placement_status",
        y="coding_skill_score",
        hue="placement_status",
        legend=False,
    )

    plt.title("Coding Skill Score by Placement Status")
    plt.xlabel("Placement Status")
    plt.ylabel("Coding Skill Score")
    plt.tight_layout()
    
    # Save the chart for the project report.
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Use a separate filename for the coding-skill chart.
    chart_path = (
        reports_dir / "coding_skills_vs_placement.png"
    ).resolve()

    try:
        plt.savefig(
            chart_path,
            dpi=300,
            bbox_inches="tight",
        )
        print(f"\nChart saved to: {chart_path}")
    finally:
        plt.close()

def analyze_internships_vs_placement(
    df: pd.DataFrame,
    reports_dir: Path,
) -> None:
    """Analyze placement rates by number of completed internships."""

    print("\n" + "=" * 60)
    print("INTERNSHIPS VS PLACEMENT RATE")
    print("=" * 60)

    # Calculate total students and placed students in each group.
    summary = df.groupby("internships_count").agg(
        total_students=("placement_status", "size"),
        placed_students=(
            "placement_status",
            lambda values: values.eq("Placed").sum(),
        ),
    )

    # Calculate placement percentage within each internship group.
    summary["placement_rate"] = (
        summary["placed_students"]
        / summary["total_students"]
        * 100
    )

    print("\nPlacement rate by internship count:")
    print(summary.round(2).to_string())

    # Plot placement rates across ordered internship counts.
    plt.figure(figsize=(9, 5))

    
    ax = sns.barplot(
        x=summary.index,
        y=summary["placement_rate"],
        hue=summary.index,
        palette="crest",
        legend=False,
    )

    ax.set_title("Placement Rate by Number of Internships")
    ax.set_xlabel("Number of Internships")
    ax.set_ylabel("Placement Rate (%)")
    ax.set_ylim(0, 100)

    # Label each bar with its placement percentage.
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f%%", padding=3)

    plt.tight_layout()

    # Save this chart separately from the previous visualizations.
    reports_dir.mkdir(parents=True, exist_ok=True)
    chart_path = reports_dir / "internships_vs_placement_rate.png"

    try:
        plt.savefig(chart_path, dpi=300, bbox_inches="tight")
        print(f"\nChart saved to: {chart_path.resolve()}")
    finally:
        plt.close()


def analyze_projects_vs_placement(
    df: pd.DataFrame,
    reports_dir: Path,
) -> None:
    """Analyze placement rates by number of completed projects."""

    print("\n" + "=" * 60)
    print("PROJECTS VS PLACEMENT RATE")
    print("=" * 60)

    # Count total and placed students for each project count.
    summary = df.groupby("projects_count").agg(
        total_students=("placement_status", "size"),
        placed_students=(
            "placement_status",
            lambda values: values.eq("Placed").sum(),
        ),
    )

    # Calculate the placement rate for each group.
    summary["placement_rate"] = (
        summary["placed_students"]
        / summary["total_students"]
        * 100
    )

    print("\nPlacement rate by project count:")
    print(summary.round(2).to_string())

    # Create a colorful bar chart.
    plt.figure(figsize=(10, 5))

    ax = sns.barplot(
        x=summary.index,
        y=summary["placement_rate"],
        hue=summary.index,
        palette="crest",
        legend=False,
    )

    ax.set_title("Placement Rate by Number of Projects")
    ax.set_xlabel("Number of Projects")
    ax.set_ylabel("Placement Rate (%)")
    ax.set_ylim(0, 100)

    # Display the percentage above each bar.
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f%%", padding=3)

    plt.tight_layout()

    # Save the chart without overwriting other visualizations.
    reports_dir.mkdir(parents=True, exist_ok=True)
    chart_path = reports_dir / "projects_vs_placement_rate.png"

    try:
        plt.savefig(chart_path, dpi=300, bbox_inches="tight")
        print(f"\nChart saved to: {chart_path.resolve()}")
    finally:
        plt.close()


def analyze_certifications_vs_placement(
    df: pd.DataFrame,
    reports_dir: Path,
) -> None:
    """Analyze placement rates by number of certifications."""

    print("\n" + "=" * 60)
    print("CERTIFICATIONS VS PLACEMENT RATE")
    print("=" * 60)

    # Count total and placed students for each certification count.
    summary = df.groupby("certifications_count").agg(
        total_students=("placement_status", "size"),
        placed_students=(
            "placement_status",
            lambda values: values.eq("Placed").sum(),
        ),
    )

    # Calculate the placement rate for each group.
    summary["placement_rate"] = (
        summary["placed_students"]
        / summary["total_students"]
        * 100
    )

    print("\nPlacement rate by certification count:")
    print(summary.round(2).to_string())

    # Create a colorful bar chart with a different palette.
    plt.figure(figsize=(10, 5))

    ax = sns.barplot(
        x=summary.index,
        y=summary["placement_rate"],
        hue=summary.index,
        palette="flare",
        legend=False,
    )

    ax.set_title("Placement Rate by Number of Certifications")
    ax.set_xlabel("Number of Certifications")
    ax.set_ylabel("Placement Rate (%)")
    ax.set_ylim(0, 100)

    # Display the percentage above each bar.
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f%%", padding=3)

    plt.tight_layout()

    # Save the chart separately.
    reports_dir.mkdir(parents=True, exist_ok=True)
    chart_path = reports_dir / "certifications_vs_placement_rate.png"

    try:
        plt.savefig(chart_path, dpi=300, bbox_inches="tight")
        print(f"\nChart saved to: {chart_path.resolve()}")
    finally:
        plt.close()


def main() -> None:
    """Load the cleaned student dataset and run initial EDA."""

    # Resolve the project directory from this script's location.
    project_root = Path(__file__).resolve().parent.parent

    data_path = (
        project_root
        / "data"
        / "processed"
        / "student_placement_prediction_cleaned.csv"
    )
    reports_dir = project_root / "reports"

    # Stop with a clear error if the processed dataset is missing.
    if not data_path.exists():
        raise FileNotFoundError(
            f"Cleaned student dataset not found: {data_path}"
        )

    # Load the cleaned dataset.
    df = pd.read_csv(data_path)

    # Check that the required column exists.
    if "placement_status" not in df.columns:
        raise KeyError("Required column 'placement_status' is missing.")

    # Run the first analysis.
    analyze_placement_distribution(df, reports_dir)

    # Run the second analysis.
    analyze_cgpa_vs_placement(df, reports_dir)

    # Run the third analysis.
    analyze_coding_skills_vs_placement(df, reports_dir)

    # Run the fourth analysis.
    analyze_internships_vs_placement(df, reports_dir)

    # Run the fifth analysis.
    analyze_projects_vs_placement(df, reports_dir)

    # Run the sixth analysis.
    analyze_certifications_vs_placement(df, reports_dir)
if __name__ == "__main__":
    main()
