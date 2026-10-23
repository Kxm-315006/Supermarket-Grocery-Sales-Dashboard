import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Supermarket Sales Dashboard", page_icon="🛒", layout="wide")
st.title("🛒 Supermarket Grocery Sales Dashboard")
st.caption("Interactive sales, product-category, outlet and visibility analysis based on the supplied BlinkIT grocery dataset.")

@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file) if uploaded_file.name.lower().endswith(".csv") else pd.read_excel(uploaded_file)
    else:
        base = Path(__file__).parent
        csv_path = base / "BlinkIT_Grocery_Data.csv"
        xlsx_path = base / "BlinkIT Grocery Data.xlsx"
        data = pd.read_csv(csv_path) if csv_path.exists() else pd.read_excel(xlsx_path)
    data.columns = data.columns.str.strip()
    data["Item Fat Content"] = data["Item Fat Content"].replace({"LF": "Low Fat", "low fat": "Low Fat", "reg": "Regular"})
    return data

with st.sidebar:
    st.header("Dashboard controls")
    uploaded = st.file_uploader("Optional: upload the dataset", type=["csv", "xlsx"])
    data = load_data(uploaded)
    categories = sorted(data["Item Type"].dropna().unique())
    outlets = sorted(data["Outlet Type"].dropna().unique())
    selected_categories = st.multiselect("Product categories", categories, default=categories)
    selected_outlets = st.multiselect("Outlet types", outlets, default=outlets)
    fat_types = sorted(data["Item Fat Content"].dropna().unique())
    selected_fat = st.multiselect("Fat content", fat_types, default=fat_types)
    locations = sorted(data["Outlet Location Type"].dropna().unique())
    selected_locations = st.multiselect("Outlet location tiers", locations, default=locations)

filtered = data[
    data["Item Type"].isin(selected_categories)
    & data["Outlet Type"].isin(selected_outlets)
    & data["Item Fat Content"].isin(selected_fat)
    & data["Outlet Location Type"].isin(selected_locations)
].copy()

if filtered.empty:
    st.warning("No records match the selected filters. Please broaden your selection.")
    st.stop()

total_sales = filtered["Sales"].sum()
avg_sales = filtered["Sales"].mean()
avg_visibility = filtered["Item Visibility"].mean()
median_sales = filtered["Sales"].median()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total sales", f"{total_sales:,.2f}")
c2.metric("Average sales / record", f"{avg_sales:,.2f}")
c3.metric("Average item visibility", f"{avg_visibility:.5f}")
c4.metric("Median sales / record", f"{median_sales:,.2f}")

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Category analysis", "Outlet analysis", "Statistical insights"])
with tab1:
    left, right = st.columns(2)
    cat_sales = filtered.groupby("Item Type", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    left.plotly_chart(px.bar(cat_sales.head(10), x="Sales", y="Item Type", orientation="h",
                             title="Top 10 product categories by sales", template="plotly_white"), use_container_width=True)
    outlet_sales = filtered.groupby("Outlet Type", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    right.plotly_chart(px.bar(outlet_sales, x="Outlet Type", y="Sales", title="Sales by outlet type",
                              template="plotly_white"), use_container_width=True)
    fat = filtered.groupby(["Outlet Identifier", "Item Fat Content"], as_index=False)["Sales"].sum()
    st.plotly_chart(px.bar(fat, x="Outlet Identifier", y="Sales", color="Item Fat Content", barmode="group",
                           title="Low Fat vs Regular sales by outlet", template="plotly_white"), use_container_width=True)

with tab2:
    cat = filtered.groupby("Item Type", as_index=False).agg(
        Total_Sales=("Sales", "sum"), Average_Sales=("Sales", "mean"), Records=("Sales", "size")
    ).sort_values("Total_Sales", ascending=False)
    top4_share = cat.head(4)["Total_Sales"].sum() / total_sales * 100
    st.metric("Share of sales from top 4 categories", f"{top4_share:.2f}%")
    low_category = cat.sort_values("Total_Sales").iloc[0]
    high_category = cat.iloc[0]
    st.write(f"**Highest sales:** {high_category['Item Type']} ({high_category['Total_Sales']:,.2f})")
    st.write(f"**Lowest sales:** {low_category['Item Type']} ({low_category['Total_Sales']:,.2f})")
    a, b = st.columns(2)
    a.plotly_chart(px.bar(cat, x="Item Type", y="Total_Sales", title="Total sales by product category",
                          template="plotly_white"), use_container_width=True)
    b.plotly_chart(px.treemap(cat, path=["Item Type"], values="Total_Sales", title="Category contribution to sales"),
                   use_container_width=True)
    st.dataframe(cat, use_container_width=True, hide_index=True)
    pivot = filtered.pivot_table(index="Item Type", columns="Outlet Type", values="Sales", aggfunc="sum", fill_value=0)
    st.plotly_chart(px.imshow(pivot, aspect="auto", color_continuous_scale="Blues",
                              title="Category sales across outlet types",
                              labels=dict(x="Outlet type", y="Product category", color="Sales")),
                    use_container_width=True)

with tab3:
    outlet = filtered.groupby(["Outlet Identifier", "Outlet Type", "Outlet Location Type"], as_index=False).agg(
        Total_Sales=("Sales", "sum"), Average_Sales=("Sales", "mean"), Records=("Sales", "size")
    )
    a, b = st.columns(2)
    a.plotly_chart(px.bar(outlet, x="Outlet Identifier", y="Total_Sales", color="Outlet Type",
                          title="Sales by outlet", template="plotly_white"), use_container_width=True)
    b.plotly_chart(px.box(filtered, x="Outlet Type", y="Sales", color="Outlet Type",
                          title="Record-level sales distribution by outlet type", template="plotly_white"),
                   use_container_width=True)
    st.dataframe(outlet.sort_values("Total_Sales", ascending=False), use_container_width=True, hide_index=True)
    location_summary = filtered.groupby("Outlet Location Type", as_index=False).agg(
        Total_Sales=("Sales", "sum"), Average_Sales=("Sales", "mean"), Records=("Sales", "size")
    )
    st.plotly_chart(px.bar(location_summary, x="Outlet Location Type", y="Total_Sales",
                           title="Sales by outlet location tier", template="plotly_white"), use_container_width=True)

with tab4:
    sales = filtered["Sales"]
    stats = pd.DataFrame({
        "Statistic": ["Count", "Mean", "Median", "Standard deviation", "Variance", "Minimum",
                      "25th percentile", "75th percentile", "Maximum"],
        "Sales": [sales.count(), sales.mean(), sales.median(), sales.std(), sales.var(), sales.min(),
                  sales.quantile(.25), sales.quantile(.75), sales.max()]
    })
    st.dataframe(stats, use_container_width=True, hide_index=True)
    q1, q3 = sales.quantile([.25, .75])
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outliers = filtered[(sales < low) | (sales > high)]
    st.write(f"IQR thresholds: below **{low:,.2f}** or above **{high:,.2f}**. Flagged records: **{len(outliers):,}**.")
    a, b = st.columns(2)
    a.plotly_chart(px.histogram(filtered, x="Sales", nbins=40, title="Sales distribution",
                                template="plotly_white"), use_container_width=True)
    b.plotly_chart(px.scatter(filtered, x="Item Visibility", y="Sales", opacity=.45,
                              title="Product visibility vs sales", trendline="ols", template="plotly_white"),
                   use_container_width=True)
    st.caption("A scatter trend line describes association, not causation. IQR flags are statistical indicators, not proof of data errors.")
    st.dataframe(outliers.sort_values("Sales", ascending=False), use_container_width=True, hide_index=True)

st.divider()
st.download_button("Download filtered data as CSV", filtered.to_csv(index=False).encode("utf-8"),
                   "filtered_supermarket_sales.csv", "text/csv")
st.caption(f"Showing {len(filtered):,} of {len(data):,} records after filters.")
