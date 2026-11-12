# Placement Skills Gap Analytics Dashboard

A data analytics project that studies student placement outcomes and technology skills appearing in job records. The project uses Python for data inspection, cleaning and exploratory analysis, and presents the findings through Excel and Power BI dashboards.

## Project objective

To explore which student preparation indicators are associated with placement outcomes and which technical skills appear in the industry job dataset, then compare the findings at an analytical level to identify potential skill gaps.

> **Scope:** This is a descriptive analytics project. The analysis identifies patterns and associations in the supplied datasets; it does not establish that a particular skill or student attribute causes placement.

## Project datasets

The project uses two datasets. They are cleaned and analyzed independently; student-level records are not joined to job-level records because there is no verified common key.

### 1. Student Placement Prediction Dataset

- **Source:** Kaggle
- **Dataset page:** [Student Placement Prediction Dataset search on Kaggle](https://www.kaggle.com/datasets?search=Student+Placement+Prediction+Dataset)
- **Purpose:** Explore student attributes and their relationship with placement outcomes.
- **Example analysis areas:** placement status, CGPA, coding skill score, internships, backlogs, aptitude and other preparation indicators.
- **Attribution and licence:** Refer to the original dataset page for the creator's attribution and applicable licence or terms. Confirm these details before redistribution.

### 2. India Tech Career Intelligence

- **Source:** Mendeley Data
- **Dataset page:** [India Tech Career Intelligence](https://data.mendeley.com/datasets/h2rmbfr68t/1)
- **Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0), as stated for the dataset.
- **Purpose:** Explore job categories, technical domains, experience levels and technical skills listed in job records.
- **Attribution:** Credit the original dataset author(s), link to the dataset page and retain the applicable licence information.

## Project workflow

1. **Data inspection** — inspect dataset structure, column names, data types and data quality.
2. **Data quality checks** — check missing values, duplicate records and relevant field consistency.
3. **Data cleaning** — prepare each dataset independently and retain fields needed for analysis.
4. **Exploratory data analysis** — calculate summary statistics and examine placement and industry-skill patterns.
5. **Dashboard preparation** — build Excel and Power BI dashboards from the prepared data.
6. **Interpretation** — compare student-side and industry-side findings without merging their underlying records.

## Dashboards

The `dashboard/` folder contains the final dashboard deliverables:

| File | Description |
|---|---|
| `Excel_Dashboard.xlsx` | Excel dashboard and analysis workbook. |
| `PowerBI_Dashboard.pbix` | **Complete Power BI report**, including its report pages, visuals, model, relationships, measures and imported data. |

### Opening the Power BI dashboard

1. Download the `.pbix` file from the GitHub `dashboard/` folder.
2. Open it using **Microsoft Power BI Desktop**.
3. The report is intended to open with its imported data; a separate dataset reconnection should not normally be needed to view the saved report.

The complete `.pbix` file is intentionally included in this repository. Its current file size is approximately 22 MB, which is below GitHub's 100 MB per-file limit. It is not a PBIT template.

## Repository structure

```text
placement-skills-gap-dashboard/
├── dashboard/
│   ├── Excel_Dashboard.xlsx
│   └── PowerBI_Dashboard.pbix
├── data/
│   ├── raw/                 # Local source datasets; not committed
│   └── processed/           # Local cleaned datasets; not committed
├── notebooks/               # Jupyter notebooks for analysis
├── reports/                 # Project reports and supporting documents
├── .gitignore
├── README.md
└── requirements.txt
```

The folder contents may evolve as the project is developed. The `.venv/` environment and local dataset files are excluded from version control.

## Tools and technologies

- **Python** — data inspection, cleaning and analysis
- **Pandas and NumPy** — data manipulation and numerical analysis
- **Matplotlib and Seaborn** — exploratory data visualisation
- **Jupyter Notebook** — interactive analysis
- **Microsoft Excel** — spreadsheet analysis and dashboard
- **Microsoft Power BI Desktop** — interactive report and dashboard
- **Git and GitHub** — version control and project hosting

## Reproducing the Python analysis

1. Install a compatible Python 3 environment.
2. Clone or download this repository.
3. Create and activate a virtual environment.
4. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Download the two source datasets from their original pages and place the files in the appropriate local `data/raw/` directory.
6. Run the notebooks in `notebooks/` in the intended order, or follow the sequence documented in the notebooks.
7. Keep generated or cleaned CSV files in `data/processed/`.

The source datasets are not bundled in this repository. Exact source filenames and any required local file paths should be checked in the notebooks before running them.

## Data handling and limitations

- Raw and processed CSV datasets are kept out of GitHub to avoid unnecessarily large repository uploads and to respect source dataset terms.
- The final Excel dashboard workbook is an intentional exception and is included in `dashboard/`.
- The complete Power BI `.pbix` report is intentionally included in `dashboard/`.
- The two datasets are analyzed independently. Their results are compared conceptually; records are not merged row by row.
- The industry dataset's listed skills reflect the supplied dataset and should not be interpreted as a complete measure of the entire technology job market.
- Interpretations are descriptive and should not be treated as causal or predictive conclusions.
- Dataset reuse and redistribution remain subject to the original creators' licences and terms.

## Acknowledgements

We acknowledge the original creators and providers of the datasets:

1. [Student Placement Prediction Dataset — Kaggle](https://www.kaggle.com/datasets?search=Student+Placement+Prediction+Dataset)
2. [India Tech Career Intelligence — Mendeley Data](https://data.mendeley.com/datasets/h2rmbfr68t/1)

Please consult the original dataset pages for complete creator attribution and licence details.

## Disclaimer

This project is developed for educational and analytical purposes. Dataset ownership and reuse rights remain with the respective creators and are governed by their original licences and terms.
