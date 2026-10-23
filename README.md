# Supermarket Grocery Sales Dashboard

An interactive data analytics project built around the supplied BlinkIT grocery sales dataset. It includes a Streamlit dashboard and an Excel analysis workbook.

## Objectives covered
- Overall sales: total, mean, median, minimum, maximum, average visibility and record count.
- Category analysis: category sales rankings, top-four category share and category contribution.
- Outlet analysis: outlet type and outlet comparisons, Low Fat vs Regular sales, category-by-outlet comparisons.
- Statistical analysis: standard deviation, variance, quartiles, sales distribution, IQR-based outlier flags and visibility-versus-sales trend.

## Files
- `app.py` — interactive dashboard with sidebar filters and four analysis tabs.
- `BlinkIT_Grocery_Data.csv` — cleaned dataset used by the dashboard.
- `Supermarket_Sales_Analysis.xlsx` — Excel workbook with executive metrics and analysis sheets.
- `requirements.txt` — Python dependencies.

## Run locally (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit (usually `http://localhost:8501`).

## Deploy
Deploy to Streamlit Community Cloud by connecting this repository, choosing `app.py` as the main file, and allowing it to install `requirements.txt`.

## Data notes
- The source file contains 8,523 records and 12 columns.
- Fat-content labels are standardized (`LF` → `Low Fat`, `reg` → `Regular`, and lowercase `low fat` → `Low Fat`).
- The app's filters recalculate the metrics and charts dynamically.
- The IQR rule flags records below Q1 − 1.5×IQR or above Q3 + 1.5×IQR. This is a statistical flag, not proof of data error.
- Product visibility and sales analysis is descriptive; correlation does not establish causation.
- Sales units/currency are not specified in the provided requirements, so the dashboard does not assume a currency symbol.

## Requirement source
The analysis follows the uploaded `Supermarket Sales Analysis Dashboard` task brief: overall performance, category contribution, outlet comparisons, visibility relationship, and sales statistical analysis.
