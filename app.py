import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Vehicle Recall Dashboard", layout="wide")

# -----------------------------
# DARK UI STYLE
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #0B0F19;
    color: #E5E7EB;
}
h1, h2, h3 {
    color: #3B82F6;
}
</style>
""", unsafe_allow_html=True)

st.title("🚗 VEHICLE RECALL DATA ANALYSIS")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("data/cleaned_vehicle_recall_data_updated.csv")

df["Recall Notification Date"] = pd.to_datetime(df["Recall Notification Date"], errors="coerce")
df["Recall Year"] = df["Recall Notification Date"].dt.year

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

# Manufacturer filter
manufacturer = st.sidebar.multiselect(
    "Manufacturer",
    df["Recall Manufacturer"].dropna().unique()
)

# Recall Type filter
recall_type = st.sidebar.multiselect(
    "Recall Type",
    df["Recall Type"].dropna().unique()
)

# -----------------------------
# YEAR RANGE FILTER (NEW)
# -----------------------------
st.sidebar.subheader("Year Range Filter")

min_year = int(df["Recall Year"].min())
max_year = int(df["Recall Year"].max())

year_range = st.sidebar.slider(
    "Select Year Range",
    min_year,
    max_year,
    (min_year, max_year)
)

# -----------------------------
# APPLY FILTERS
# -----------------------------
filtered_df = df.copy()

if manufacturer:
    filtered_df = filtered_df[filtered_df["Recall Manufacturer"].isin(manufacturer)]

if recall_type:
    filtered_df = filtered_df[filtered_df["Recall Type"].isin(recall_type)]

# Apply year filter
filtered_df = filtered_df[
    (filtered_df["Recall Year"] >= year_range[0]) &
    (filtered_df["Recall Year"] <= year_range[1])
]

# -----------------------------
# KPI SECTION
# -----------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(filtered_df))
col2.metric("Total Impact", f"{int(filtered_df['Estimated Units'].sum()):,}")
col3.metric("Avg Impact", int(filtered_df["Estimated Units"].mean()))

st.markdown("---")

# -----------------------------
# COMMON STYLE FUNCTION
# -----------------------------
def style_fig(fig):
    fig.update_layout(
        plot_bgcolor="#0B0F19",
        paper_bgcolor="#0B0F19",
        font=dict(color="#E5E7EB"),
        xaxis_tickangle=-45
    )
    return fig

# -----------------------------
# 1. RECALL TYPE ANALYSIS
# -----------------------------
st.subheader("Recall Type Analysis")

recall_df = filtered_df["Recall Type"].value_counts().reset_index()
recall_df.columns = ["Recall Type", "Count"]

fig1 = px.bar(
    recall_df,
    x="Recall Type",
    y="Count",
    color="Recall Type",
    color_discrete_sequence=["#3B82F6", "#22C55E", "#F59E0B", "#EF4444"]
)

st.plotly_chart(style_fig(fig1), use_container_width=True)

# -----------------------------
# 2. COMPONENT ANALYSIS
# -----------------------------
st.subheader("Component Analysis")

comp_df = filtered_df["Main Component"].value_counts().head(10).reset_index()
comp_df.columns = ["Component", "Count"]

fig2 = px.bar(
    comp_df,
    x="Component",
    y="Count",
    color="Count",
    color_continuous_scale="Blues"
)

st.plotly_chart(style_fig(fig2), use_container_width=True)

# -----------------------------
# 3. MANUFACTURER ANALYSIS
# -----------------------------
st.subheader("Manufacturer Analysis")

manu_df = filtered_df["Recall Manufacturer"].value_counts().head(10).reset_index()
manu_df.columns = ["Manufacturer", "Count"]

fig3 = px.bar(
    manu_df,
    x="Manufacturer",
    y="Count",
    color="Count",
    color_continuous_scale="Viridis"
)

st.plotly_chart(style_fig(fig3), use_container_width=True)

# -----------------------------
# 4. VEHICLE MAKE ANALYSIS
# -----------------------------
st.subheader("Vehicle Make Analysis")

make_df = filtered_df["Vehicle Make"].value_counts().head(10).reset_index()
make_df.columns = ["Vehicle Make", "Count"]

fig4 = px.bar(
    make_df,
    x="Vehicle Make",
    y="Count",
    color="Count",
    color_continuous_scale="Teal"
)

st.plotly_chart(style_fig(fig4), use_container_width=True)

# -----------------------------
# 5. MODEL YEAR ANALYSIS
# -----------------------------
st.subheader("Model Year Analysis")

year_df = filtered_df["Model Year"].value_counts().head(10).reset_index()
year_df.columns = ["Model Year", "Count"]

fig5 = px.bar(
    year_df,
    x="Model Year",
    y="Count",
    color="Count",
    color_continuous_scale="Plasma"
)

st.plotly_chart(style_fig(fig5), use_container_width=True)

# -----------------------------
# 6. HARDWARE VS SOFTWARE
# -----------------------------
st.subheader("Hardware vs Software Analysis")

issue_df = filtered_df["Issue Type"].value_counts().reset_index()
issue_df.columns = ["Issue Type", "Count"]

fig6 = px.pie(
    issue_df,
    names="Issue Type",
    values="Count",
    color_discrete_sequence=["#22C55E", "#EF4444"]
)

st.plotly_chart(fig6, use_container_width=True)

# -----------------------------
# 7. IMPACT ANALYSIS
# -----------------------------
st.subheader("Impact Analysis")

impact_df = filtered_df.groupby("Main Component")["Estimated Units"].sum().sort_values(ascending=False).head(10).reset_index()

fig7 = px.bar(
    impact_df,
    x="Main Component",
    y="Estimated Units",
    color="Estimated Units",
    color_continuous_scale="Turbo"
)

st.plotly_chart(style_fig(fig7), use_container_width=True)

# -----------------------------
# 8. COMPONENT SEVERITY
# -----------------------------
st.subheader("Component Severity Analysis")

comp_impact_df = filtered_df.groupby("Main Component")["Estimated Units"].mean().sort_values(ascending=False).head(10).reset_index()

fig8 = px.bar(
    comp_impact_df,
    x="Main Component",
    y="Estimated Units",
    color="Estimated Units",
    color_continuous_scale="Inferno"
)

st.plotly_chart(style_fig(fig8), use_container_width=True)

# -----------------------------
# 9. MANUFACTURER SEVERITY
# -----------------------------
st.subheader("Manufacturer Severity Analysis")

manu_severity = filtered_df.groupby("Recall Manufacturer")["Estimated Units"].mean().sort_values(ascending=False).head(10).reset_index()

fig9 = px.bar(
    manu_severity,
    x="Recall Manufacturer",
    y="Estimated Units",
    color="Estimated Units",
    color_continuous_scale="Magma"
)

st.plotly_chart(style_fig(fig9), use_container_width=True)

# -----------------------------
# 10. TREND OVER TIME
# -----------------------------
st.subheader("Recall Trend Over Time")

trend_df = filtered_df.groupby("Recall Year")["Estimated Units"].sum().reset_index()

fig10 = px.line(
    trend_df,
    x="Recall Year",
    y="Estimated Units",
    markers=True
)

fig10.update_traces(line_color="#3B82F6")

st.plotly_chart(style_fig(fig10), use_container_width=True)