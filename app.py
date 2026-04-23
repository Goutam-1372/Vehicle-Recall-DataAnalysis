import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG (BLOOMBERG STYLE)
# -----------------------------
st.set_page_config(
    page_title="Vehicle Recall Data Analysis",
    layout="wide"
)

# -----------------------------
# DARK UI STYLE
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #0B0F19;
    color: #E5E7EB;
}

.block-container {
    padding: 2rem;
}

section[data-testid="stSidebar"] {
    background-color: #0F172A;
}

h1, h2, h3 {
    color: #60A5FA;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("data/cleaned_vehicle_recall_data_updated.csv")

df["Recall Notification Date"] = pd.to_datetime(df["Recall Notification Date"], errors="coerce")

# -----------------------------
# TITLE
# -----------------------------
st.title(" VEHICLE RECALL DATA ANALYSIS")

st.markdown("---")

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("FILTER ENGINE")

date_range = st.sidebar.date_input(
    "Date Range",
    [df["Recall Notification Date"].min(), df["Recall Notification Date"].max()]
)

manufacturer_filter = st.sidebar.multiselect(
    "Manufacturer",
    df["Recall Manufacturer"].dropna().unique()
)

recall_type_filter = st.sidebar.multiselect(
    "Recall Type",
    df["Recall Type"].dropna().unique()
)

# -----------------------------
# FILTER DATA
# -----------------------------
filtered_df = df.copy()

if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["Recall Notification Date"] >= pd.to_datetime(date_range[0])) &
        (filtered_df["Recall Notification Date"] <= pd.to_datetime(date_range[1]))
    ]

if manufacturer_filter:
    filtered_df = filtered_df[filtered_df["Recall Manufacturer"].isin(manufacturer_filter)]

if recall_type_filter:
    filtered_df = filtered_df[filtered_df["Recall Type"].isin(recall_type_filter)]

# -----------------------------
# KPI SECTION
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("TOTAL RECORDS", len(filtered_df))
col2.metric("TOTAL IMPACT", f"{int(filtered_df['Estimated Units'].sum()):,}")
col3.metric("AVG IMPACT", int(filtered_df["Estimated Units"].mean()))
col4.metric("PEAK YEAR", filtered_df["Recall Year"].value_counts().idxmax())

st.markdown("---")

# -----------------------------
# 1. RECALL TYPE DISTRIBUTION
# -----------------------------
st.subheader("RECALL TYPE DISTRIBUTION")

recall_df = filtered_df["Recall Type"].value_counts().reset_index()
recall_df.columns = ["Recall Type", "Count"]

fig1 = px.bar(
    recall_df,
    x="Recall Type",
    y="Count",
    color="Recall Type",
    color_discrete_sequence=["#3B82F6", "#22C55E", "#F97316", "#EF4444"]
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# 2. ISSUE TYPE
# -----------------------------
st.subheader("SYSTEM FAILURE TYPE")

issue_df = filtered_df["Issue Type"].value_counts().reset_index()
issue_df.columns = ["Issue Type", "Count"]

fig2 = px.pie(
    issue_df,
    names="Issue Type",
    values="Count",
    color_discrete_sequence=["#22C55E", "#EF4444"]
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# 3. TOP DEFECTIVE COMPONENTS
# -----------------------------
st.subheader("TOP DEFECTIVE COMPONENTS")

comp_df = filtered_df["Main Component"].value_counts().head(10).reset_index()
comp_df.columns = ["Component", "Count"]

comp_df["Component"] = comp_df["Component"].astype(str).str[:35]

fig3 = px.bar(
    comp_df,
    x="Component",
    y="Count",
    color="Count",
    color_continuous_scale="Blues"
)

fig3.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# 4. IMPACT BY COMPONENT
# -----------------------------
st.subheader("IMPACT BY COMPONENT (UNITS AFFECTED)")

impact_df = filtered_df.groupby("Main Component")["Estimated Units"].sum().sort_values(ascending=False).head(10).reset_index()

impact_df["Main Component"] = impact_df["Main Component"].astype(str).str[:35]

fig4 = px.bar(
    impact_df,
    x="Main Component",
    y="Estimated Units",
    color="Estimated Units",
    color_continuous_scale="Turbo"
)

fig4.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# 5. TOP MANUFACTURERS (COUNT)
# -----------------------------
st.subheader("TOP MANUFACTURERS")

manu_df = filtered_df["Recall Manufacturer"].value_counts().head(10).reset_index()
manu_df.columns = ["Manufacturer", "Count"]

fig5 = px.bar(
    manu_df,
    x="Manufacturer",
    y="Count",
    color="Manufacturer",
    color_discrete_sequence=["#3B82F6", "#22C55E", "#F97316"]
)

fig5.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig5, use_container_width=True)

# -----------------------------
# 6. TREND OVER TIME
# -----------------------------
st.subheader("RECALL TREND OVER TIME")

year_df = filtered_df.groupby("Recall Year")["Estimated Units"].sum().reset_index()

fig6 = px.line(
    year_df,
    x="Recall Year",
    y="Estimated Units",
    markers=True
)

fig6.update_traces(line_color="#3B82F6")

st.plotly_chart(fig6, use_container_width=True)

# -----------------------------
# 7. NEW: AVG IMPACT PER MANUFACTURER
# -----------------------------
st.subheader("AVERAGE IMPACT PER MANUFACTURER")

avg_impact_df = filtered_df.groupby("Recall Manufacturer")["Estimated Units"].mean().sort_values(ascending=False).head(10).reset_index()

fig7 = px.bar(
    avg_impact_df,
    x="Recall Manufacturer",
    y="Estimated Units",
    color="Estimated Units",
    color_continuous_scale="Plasma"
)

fig7.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig7, use_container_width=True)

# -----------------------------
# INSIGHTS
# -----------------------------
st.markdown("## 📌 SYSTEM INSIGHTS")

st.success(f"""
• Most common component: {filtered_df['Main Component'].value_counts().idxmax()}  
• Highest impact manufacturer: {filtered_df.groupby('Recall Manufacturer')['Estimated Units'].sum().idxmax()}  
• Peak recall year: {filtered_df['Recall Year'].value_counts().idxmax()}  
• Total impact: {int(filtered_df['Estimated Units'].sum()):,}
""")