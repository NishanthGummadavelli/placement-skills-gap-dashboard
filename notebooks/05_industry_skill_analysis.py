

"""
Industry skill-demand analysis for the Placement Skills Gap Dashboard.

Inspects the skills column before calculating individual skill frequencies.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter


def inspect_skills_column(df: pd.DataFrame) -> None:
    """Inspect how extracted skills are represented in the dataset."""

    print("\n" + "=" * 60)
    print("INSPECTING INDUSTRY SKILLS")
    print("=" * 60)

    # Display representative values before parsing the skill lists.
    print("\nSample skills_extracted values:")
    print(
        df["skills_extracted"]
        .dropna()
        .head(15)
        .to_string(index=False)
    )

    print("\nData type:", df["skills_extracted"].dtype)
    print("Missing values:", df["skills_extracted"].isna().sum())
    print("Unique skill-list patterns:", df["skills_extracted"].nunique())



def analyze_top_skills(
    df: pd.DataFrame,
    reports_dir: Path,
) -> None:
    """Count individual skill mentions and plot the most frequent skills."""

    print("\n" + "=" * 60)
    print("TOP 10 MOST DEMANDED TECHNICAL SKILLS")
    print("=" * 60)

    # Split comma-separated skill lists into individual skills.
    skills = (
        df["skills_extracted"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
    )

    # Remove empty entries and normalize skill names.
    skills = skills[skills.ne("")]
    skills = skills.str.casefold()

    # Count how many job records mention each skill.
    skill_counts = skills.value_counts().head(10)

    print("\nTop 10 skills by number of mentions:")
    print(skill_counts.to_string())

    # Create the reports directory if necessary.
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Create a colorful horizontal bar chart.
    plt.figure(figsize=(10, 6))

    ax = sns.barplot(
        x=skill_counts.values,
        y=skill_counts.index,
        hue=skill_counts.index,
        palette="mako",
        legend=False,
    )

    ax.set_title("Top 10 Most Demanded Technical Skills")
    ax.set_xlabel("Number of Job Records Mentioning the Skill")
    ax.set_ylabel("Technical Skill")

    # Label bars with their counts.
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=4)

    plt.tight_layout()

    # Save the chart for the project report.
    chart_path = reports_dir / "top_10_industry_skills.png"

    try:
        plt.savefig(chart_path, dpi=300, bbox_inches="tight")
        print(f"\nChart saved to: {chart_path.resolve()}")
    finally:
        plt.close()


def inspect_job_categories(df: pd.DataFrame) -> None:
    """Inspect job categories and their associated skill-list patterns."""

    print("\n" + "=" * 60)
    print("JOB CATEGORIES AND SKILL PATTERNS")
    print("=" * 60)

    # Show the number of job records in each category.
    print("\nJob records by category:")
    print(df["job_category"].value_counts().to_string())

    # Check how many distinct skill lists occur in each category.
    print("\nUnique skill-list patterns by category:")
    print(
        df.groupby("job_category")["skills_extracted"]
        .nunique()
        .to_string()
    )

    # Show representative categories and their skill lists.
    print("\nSample category-to-skill mapping:")
    mapping = df[
        ["job_category", "skills_extracted"]
    ].drop_duplicates()

    print(mapping.to_string(index=False, max_rows=30))


def analyze_skill_coverage_by_category(
    df: pd.DataFrame,
    reports_dir: Path
) -> None:
    """Plot the number of distinct listed skills for each job category."""

    # Count the skills listed for each category.
    category_skills = df[
        ["job_category", "skills_extracted"]
    ].drop_duplicates(subset=["job_category"])

    category_skills = category_skills.copy()
    category_skills["skill_count"] = (
        category_skills["skills_extracted"]
        .str.split(",")
        .apply(lambda skills: len([s.strip() for s in skills if s.strip()]))
    )

    category_skills = category_skills.sort_values(
        "skill_count", ascending=True
    )

    # Create and save the horizontal bar chart.
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=category_skills,
        x="skill_count",
        y="job_category",
        hue="job_category",
        palette="viridis",
        legend=False
    )

    plt.title("Number of Listed Technical Skills by Job Category")
    plt.xlabel("Number of Listed Skills")
    plt.ylabel("Job Category")
    plt.tight_layout()

    reports_dir.mkdir(parents=True, exist_ok=True)
    output_path = reports_dir / "skill_coverage_by_category.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"\nSkill coverage chart saved to: {output_path}")
    print(category_skills[["job_category", "skill_count"]].to_string(index=False))


def analyze_job_category_distribution(
    df: pd.DataFrame,
    reports_dir: Path
) -> None:
    """Plot the number of job records in each industry category."""

    # Count job records for each category.
    category_counts = (
        df["job_category"]
        .value_counts()
        .sort_values(ascending=True)
    )

    # Create a horizontal bar chart.
    plt.figure(figsize=(10, 6))
    sns.barplot(
        x=category_counts.values,
        y=category_counts.index,
        hue=category_counts.index,
        palette="viridis",
        legend=False
    )

    # Add titles and axis labels.
    plt.title("Distribution of Job Records by Category", fontsize=14)
    plt.xlabel("Number of Job Records")
    plt.ylabel("Job Category")

    # Add record counts at the ends of the bars.
    for index, count in enumerate(category_counts.values):
        plt.text(count + 100, index, f"{count:,}", va="center")

    plt.tight_layout()

    # Save the chart in the reports directory.
    reports_dir.mkdir(parents=True, exist_ok=True)
    output_path = reports_dir / "job_category_distribution.png"

    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"\nJob category distribution chart saved to: {output_path}")
    print("\nJob records by category:")
    print(category_counts.sort_values(ascending=False).to_string())


def analyze_skill_frequency_by_category(
    df: pd.DataFrame,
    reports_dir: Path
) -> None:
    """Plot the most frequently listed skills within each job category."""

    # Split comma-separated skills into individual skill mentions.
    skill_data = df[["job_category", "skills_extracted"]].copy()
    skill_data["skill"] = skill_data["skills_extracted"].str.split(",")
    skill_data = skill_data.explode("skill")
    skill_data["skill"] = skill_data["skill"].str.strip()

    # Remove empty skill names and standardize capitalization.
    skill_data = skill_data[skill_data["skill"] != ""].copy()
    skill_data["skill"] = skill_data["skill"].str.title()

    # Count mentions within each category.
    skill_counts = (
        skill_data.groupby(["job_category", "skill"])
        .size()
        .reset_index(name="mention_count")
    )

    # Keep the five most-mentioned skills per category.
    top_skills = (
        skill_counts.sort_values(
            ["job_category", "mention_count", "skill"],
            ascending=[True, False, True]
        )
        .groupby("job_category")
        .head(5)
    )

    # Create a separate chart for each category.
    categories = sorted(top_skills["job_category"].unique())
    fig, axes = plt.subplots(
        nrows=3, ncols=2, figsize=(14, 15)
    )

    for ax, category in zip(axes.flat, categories):
        category_data = top_skills[
            top_skills["job_category"] == category
        ].sort_values("mention_count", ascending=True)

        sns.barplot(
            data=category_data,
            x="mention_count",
            y="skill",
            hue="skill",
            palette="viridis",
            legend=False,
            ax=ax
        )
        ax.set_title(category)
        ax.set_xlabel("Number of Job Records Mentioning Skill")
        ax.set_ylabel("Technical Skill")

    fig.suptitle(
        "Top Technical Skills by Job Category",
        fontsize=16,
        y=1.01
    )
    fig.tight_layout()

    # Save the combined chart.
    reports_dir.mkdir(parents=True, exist_ok=True)
    output_path = reports_dir / "skill_frequency_by_category.png"
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"\nSkill frequency chart saved to: {output_path}")


def inspect_salary_data(df: pd.DataFrame) -> None:
    """Check salary columns before performing salary analysis."""

    salary_columns = ["salary_minimum", "salary_maximum"]

    print("\n" + "=" * 60)
    print("SALARY DATA INSPECTION")
    print("=" * 60)

    # Check that the required columns exist.
    missing_columns = [
        column for column in salary_columns
        if column not in df.columns
    ]

    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        return

    # Convert salary columns to numeric for inspection.
    salary_data = df[salary_columns].apply(
        pd.to_numeric, errors="coerce"
    )

    print("\nSalary data types:")
    print(salary_data.dtypes)

    print("\nSalary summary:")
    print(salary_data.describe().round(2).to_string())

    print("\nMissing values:")
    print(salary_data.isna().sum().to_string())

    print("\nSalary values by job category:")
    print(
        df.assign(
            salary_minimum=salary_data["salary_minimum"],
            salary_maximum=salary_data["salary_maximum"]
        )
        .groupby("job_category")[
            ["salary_minimum", "salary_maximum"]
        ]
        .median()
        .round(2)
        .to_string()
    )


def analyze_salary_range_by_category(
    df: pd.DataFrame,
    reports_dir: Path
) -> None:
    """Compare median minimum and maximum salaries across job categories."""

    # Convert salary columns to numeric values.
    salary_df = df.copy()
    salary_df["salary_minimum"] = pd.to_numeric(
        salary_df["salary_minimum"], errors="coerce"
    )
    salary_df["salary_maximum"] = pd.to_numeric(
        salary_df["salary_maximum"], errors="coerce"
    )

    # Calculate median salary bounds for each category.
    summary = (
        salary_df.groupby("job_category")[
            ["salary_minimum", "salary_maximum"]
        ]
        .median()
        .sort_values("salary_minimum")
    )

    # Prepare data for grouped bars.
    plot_data = summary.reset_index().melt(
        id_vars="job_category",
        value_vars=["salary_minimum", "salary_maximum"],
        var_name="salary_type",
        value_name="median_salary"
    )

    plot_data["salary_type"] = plot_data["salary_type"].map({
        "salary_minimum": "Median Minimum Salary",
        "salary_maximum": "Median Maximum Salary"
    })

    # Create the chart.
    plt.figure(figsize=(12, 7))
    sns.barplot(
        data=plot_data,
        x="median_salary",
        y="job_category",
        hue="salary_type",
        palette="Set2"
    )

    # Display salary values in millions for easier reading.
    plt.gca().xaxis.set_major_formatter(
        FuncFormatter(lambda value, _: f"{value / 1_000_000:.1f}M")
    )
    plt.title("Median Salary Range by Job Category")
    plt.xlabel("Median Salary Value (as recorded in dataset)")
    plt.ylabel("Job Category")
    plt.legend(title="Salary Measure")
    plt.tight_layout()

    # Save the chart.
    reports_dir.mkdir(parents=True, exist_ok=True)
    output_path = reports_dir / "salary_range_by_category.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"\nSalary range chart saved to: {output_path}")
    print("\nMedian salary summary:")
    print(summary.round(2).to_string())


def analyze_salary_range_by_experience(
    df: pd.DataFrame,
    reports_dir: Path
) -> None:
    """Compare median salary bounds across experience levels."""

    # Convert salary columns to numeric values.
    salary_df = df.copy()
    for column in ["salary_minimum", "salary_maximum"]:
        salary_df[column] = pd.to_numeric(
            salary_df[column], errors="coerce"
        )

    # Remove rows missing the required analysis fields.
    salary_df = salary_df.dropna(
        subset=[
            "experience_level",
            "salary_minimum",
            "salary_maximum"
        ]
    )

    # Calculate median salary bounds by experience level.
    summary = (
        salary_df.groupby("experience_level")[
            ["salary_minimum", "salary_maximum"]
        ]
        .median()
        .sort_values("salary_minimum")
    )

    # Reshape the data for a grouped bar chart.
    plot_data = summary.reset_index().melt(
        id_vars="experience_level",
        value_vars=["salary_minimum", "salary_maximum"],
        var_name="salary_type",
        value_name="median_salary"
    )

    plot_data["salary_type"] = plot_data["salary_type"].map({
        "salary_minimum": "Median Minimum Salary",
        "salary_maximum": "Median Maximum Salary"
    })

    # Plot the salary comparison.
    plt.figure(figsize=(11, 6))
    sns.barplot(
        data=plot_data,
        x="median_salary",
        y="experience_level",
        hue="salary_type",
        palette="Set2"
    )

    # Use millions to make large values easier to read.
    from matplotlib.ticker import FuncFormatter

    plt.gca().xaxis.set_major_formatter(
        FuncFormatter(lambda value, _: f"{value / 1_000_000:.1f}M")
    )

    plt.title("Median Salary Range by Experience Level")
    plt.xlabel("Median Salary Value (as recorded in dataset)")
    plt.ylabel("Experience Level")
    plt.legend(title="Salary Measure")
    plt.tight_layout()

    # Save the chart.
    reports_dir.mkdir(parents=True, exist_ok=True)
    output_path = reports_dir / "salary_range_by_experience.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"\nSalary-by-experience chart saved to: {output_path}")
    print("\nMedian salary summary by experience level:")
    print(summary.round(2).to_string())


def main() -> None:
    """Load the cleaned industry dataset and inspect its skill column."""

    # Resolve paths relative to the project root.
    project_root = Path(__file__).resolve().parent.parent
    reports_dir = project_root / "reports"
    data_path = (
        project_root
        / "data"
        / "processed"
        / "indian_tech_career_intelligence_cleaned.csv"
    )

    # Ensure the cleaned dataset exists.
    if not data_path.exists():
        raise FileNotFoundError(
            f"Cleaned industry dataset not found: {data_path}"
        )

    df = pd.read_csv(data_path, low_memory=False)

    # Inspect the skill format before choosing a parsing method.
    if "skills_extracted" not in df.columns:
        raise KeyError("Required column 'skills_extracted' is missing.")

    inspect_skills_column(df)

    analyze_top_skills(df, project_root / "reports")

    inspect_job_categories(df)

    analyze_skill_coverage_by_category(df, reports_dir)

    analyze_job_category_distribution(df, reports_dir)

    analyze_skill_frequency_by_category(df, reports_dir)

    inspect_salary_data(df)

    analyze_salary_range_by_category(df, reports_dir)

    analyze_salary_range_by_experience(df, reports_dir)

if __name__ == "__main__":
    main()
