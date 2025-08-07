#  Brent Oil Price Change Point Analysis

This project analyzes historical Brent oil prices (1987–2022) to detect significant structural breaks using **Bayesian change point modeling with PyMC**. These breakpoints are matched with **geopolitical, economic, and OPEC-related events** to uncover the influence of real-world happenings on oil markets. An interactive **dashboard built with Flask and React** helps stakeholders explore the insights.

>  Final submission for the 10 Academy AI Mastery Week 10 Challenge (July 30–August 7, 2025)

---

## 🗂️ Project Structure

```

project\_root/
├── data/
│   ├── raw/                          # Original Brent oil price data
│   ├── processed/                    # Cleaned prices, events, log returns
│   └── external/                     # Optional macroeconomic indicators
├── results/
│   ├── figures/                      # Visualizations
│   └── change\_points.csv             # Model-detected breakpoints
├── src/
│   ├── data\_preparation/             # Cleaning logic
│   ├── analysis/                     # Bayesian modeling (PyMC)
│   ├── backend/                      # Flask backend (APIs)
├── frontend/                         # React frontend (dashboard)
│   ├── public/
│   └── src/
├── notebooks/
│   └── exploratory\_analysis.ipynb    # EDA notebook
├── reports/
│   ├── interim\_report.pdf
│   └── final\_report.pdf
├── tests/                            # Unit and API tests
│   ├── test\_preprocess.py
│   ├── test\_model.py
│   └── test\_api.py
├── requirements.txt
└── README.md

````

---

##  Task Overview

### Task 1: Laying the Foundation
- Cleaned and transformed historical oil data.
- Calculated daily **log returns** to stabilize variance.
- Collected and annotated **15 real-world events** (wars, sanctions, OPEC decisions).
- Performed **exploratory data analysis (EDA)**.

### Task 2: Bayesian Change Point Modeling
- Used **PyMC4** to implement Bayesian model for detecting structural breaks.
- Estimated date of change (`tau`), and mean/std deviations before and after.
- Matched detected change points with events.
- Saved model trace and summary to `results/`.

### Task 3: Interactive Dashboard (Flask + React)
- Built a backend using **Flask** to serve API endpoints:
  - `/log-returns`, `/change-points`, `/matched-events`
- Created a frontend using **React + Recharts**:
  -  Log return chart with **red lines** for change points and **green lines** for matched events.
  -  **Date range filters**
  -  **Event category filters and search**
  -  **Zoom & pan**
  -  **Summary statistics (mean, volatility, std dev)**

---

##  Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/emegua19/Brent-Oil-Price-Change-Analysis.git
cd Brent-Oil-Price-Change-Analysis
````

### 2. Set up virtual environment

```bash
python -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run Preprocessing

```bash
python src/data_preparation/preprocess.py
```

### 4. Run Bayesian Change Point Model

```bash
python src/analysis/change_point_model.py
```

### 5. Start the Flask Backend

```bash
python src/backend/app.py
```

API will be available at: [http://localhost:5000](http://localhost:5000)

### 6. Launch the React Frontend

```bash
cd frontend
npm install
npm start
```

Frontend will run at: [http://localhost:3000](http://localhost:3000)

---

##  Testing

Run unit and API tests:

```bash
pytest tests/ -v
```

---

##  Visual Highlights

* `price_trends.png`: Long-term oil trends
* `volatility_plot.png`: Volatility of daily log returns
* `price_with_events.png`: Annotated spikes with global events

---

##  Dependencies (selected)

* **Modeling**: `pymc3`, `theano-pymc`, `arviz`
* **Visualization**: `matplotlib`, `seaborn`, `recharts`
* **Backend**: `Flask`, `Flask-Cors`
* **Frontend**: `React`, `Recharts`
* **Testing**: `pytest`

---

## 📄 Reports

* `reports/interim_report.pdf`: EDA, assumptions, event selection
* `reports/final_report.pdf`: Change point modeling + dashboard insights

---

##  License

For educational use under **10 Academy AI Mastery Program**. Attribution required for reuse.

---

## 👤 Author

**Yitbarek Geletaw**
Brent Oil Analysis — 10 Academy (Week 10)
GitHub: [emegua19](https://github.com/emegua19)
