
# Brent Oil Price Change Point Analysis

This project analyzes historical Brent oil prices (1987–2022) to identify structural breaks using Bayesian change point detection with PyMC3. It links price changes to major geopolitical, economic, and OPEC events, providing insights for investors, policymakers, and energy companies.

This repository contains the interim submission for Task 1 of the 10 Academy AI Mastery Week 10 Challenge (July 30–August 5, 2025).

---

## Project Structure

```

project\_root/
├── data/
│   ├── raw/
│   │   └── brent\_oil\_prices.csv              # Original historical price data
│   ├── processed/
│   │   └── events.csv                        # Curated event dataset (Date, Description)
│   └── external/                             # Optional: additional macroeconomic data
├── results/
│   └── figures/
        |--trace_plots
    │       ├── price\_trends.png
    │       ├── volatility\_plot.png
    │       └── price\_with\_events.png
├── src/
│   ├── data\_preparation/
│   │   └── preprocess.py                     # Data loading & cleaning functions
│   ├── analysis/
│   │   └── change\_point\_model.py             # PyMC3 modeling logic
│   ├── utils/
│   │   └── helpers.py                        # Utility functions (dates, log returns, etc.)
│   ├── backend/
│   │   ├── app.py                            # Flask backend entry point
│   │   └── api/
│   │       └── data\_api.py                   # API routes to serve model results
│   └── frontend/
│       ├── public/
│       │   └── index.html
│       ├── src/
│       │   ├── components/
│       │   │   ├── PriceChart.jsx
│       │   │   ├── EventFilter.jsx
│       │   │   └── Dashboard.jsx
│       │   ├── App.jsx
│       │   └── index.js
│       └── package.json
├── notebooks/
│   └── exploratory\_analysis.ipynb            # EDA and insights exploration
├── reports/
│   ├── interim\_report.pdf                    # Task 1 deliverable (analysis plan, events)
│   └── final\_report.pdf                      # Final blog-style report or PDF
├── tests/
│   ├── test\_preprocess.py                    # Unit tests for data pipeline
│   ├── test\_model.py                         # Tests for modeling logic
│   └── test\_api.py                           # API endpoint tests
├── docs/
│   ├── project\_overview\.md                   # Project design, architecture
│   └── data\_sources.md
├── requirements.txt                          # Python dependencies
├── README.md                                 # Project intro, setup instructions
└── .gitignore                                # Ignore checkpoints, virtual envs, builds

````

---

## Task 1: Laying the Foundation

- **Preprocessed Data**: Loaded and cleaned `brent_oil_prices.csv`, computed log returns, and saved to `data/processed/brent_oil_log_returns.csv`.
- **Event Dataset**: Compiled 15 significant geopolitical, economic, and OPEC events (2012–2022 and earlier) in `data/processed/events.csv`.
- **Exploratory Data Analysis**:
  - Visualized trends, log returns, and events (`notebooks/exploratory_analysis.ipynb`)
  - Conducted ADF test confirming non-stationary prices and stationary log returns.
- **Workflow & Assumptions**: Described steps, assumptions (e.g., log returns stabilize data), and limitations (e.g., correlation ≠ causation) in `reports/interim_report.pdf`.

---

## Visuals

Plots saved in `results/figures/`:

- `price_trends.png`: Brent oil price trends (1987–2022)
- `volatility_plot.png`: Daily log returns with volatility clustering
- `price_with_events.png`: Prices with event markers (e.g., 2014 OPEC decision, 2022 Russia-Ukraine war)

---

## Setup

### Clone the Repository

```bash
git clone https://github.com/emegua19/Brent-Oil-Price-Change-Analysis.git
cd project_root
````

### Set Up Python Environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run Preprocessing

```bash
python src/data_preparation/preprocess.py
```

### Run Exploratory Analysis

```bash
jupyter notebook notebooks/exploratory_analysis.ipynb
```

### Run Unit Tests

```bash
PYTHONPATH=$PWD/src pytest tests/test_preprocess.py -v
```

---

## Dependencies

Key packages listed in `requirements.txt`:

* `pandas>=1.5.0`
* `numpy>=1.23.0`
* `matplotlib>=3.5.0`
* `seaborn>=0.11.0`
* `statsmodels>=0.13.0`
* `pytest>=7.0.0`

---

## Interim Submission

* **Report**: `reports/interim_report.pdf` (workflow, assumptions, event dataset)
* **Event Dataset**: `data/processed/events.csv` (15 events)
* **Code**:

  * `notebooks/exploratory_analysis.ipynb`
  * `src/data_preparation/preprocess.py`
  * `src/utils/helpers.py`
  * `tests/test_preprocess.py`
* **GitHub**: *(https://github.com/emegua19/Brent-Oil-Price-Change-Analysis.git)*

---

## Next Steps

Proceed to **Task 2**: Implement Bayesian change point model in `src/analysis/change_point_model.py` using PyMC3 to detect structural breaks and match them with real-world events.

---

## License

For educational purposes as part of **10 Academy AI Mastery**. All rights reserved.

