# Supermarket Grocery Sales Dashboard

An interactive data analytics project based on the supplied BlinkIT grocery sales dataset. Includes a Streamlit dashboard and Excel analysis workbook aligned with the project brief.

## Project objectives covered
- Overall performance: total sales, average sales per record, average item visibility, mean/median/minimum/maximum, and record count.
- Product categories: category rankings, top-four category share, category contribution, and average sales per category.
- Outlet performance: total sales by outlet type and outlet, Low Fat vs Regular sales, and category comparisons across outlet types.
- Statistical analysis: standard deviation, variance, quartiles, sales distribution, IQR-based unusual-value flags, visibility-versus-sales scatterplot and trendline.

## Repository contents
- `app.py` — interactive Streamlit app with filters and four analysis tabs.
- `BlinkIT_Grocery_Data.csv` — cleaned data used by the dashboard.
- `Supermarket_Sales_Analysis.xlsx` — Excel workbook with summary and analysis sheets.
- `BlinkIT Grocery Data.xlsx` — original supplied dataset.
- `requirements.txt` — Python dependencies.

## Run locally (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Deployment
Deploy on Streamlit Community Cloud by selecting this repository and setting `app.py` as the app entry point. Dependencies are installed from `requirements.txt`.

## Dataset notes
- The source dataset contains 8,523 records and 12 columns.
- Fat-content labels are standardized (`LF` → `Low Fat`, `reg` → `Regular`, and lowercase `low fat` → `Low Fat`).
- Filters recalculate metrics and charts dynamically.
- IQR flags are statistical indicators, not proof of errors.
- Visibility-versus-sales association does not imply causation.
- The brief does not specify currency, so no currency symbol is assumed.

## Key baseline metrics (full dataset)
- Total sales: 1,201,681.49
- Average sales per record: 140.99
- Median sales per record: 143.0128
- Average item visibility: 0.06613
- Top four categories' sales share: 50.60%
- Highest-selling category: Fruits and Vegetables
- Lowest-selling category: Seafood

Numbers are based on the uploaded dataset and rounded for readability.
