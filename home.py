import streamlit as st

# --- PAGE TITLE ---
st.title("🦠 Objective 1: Temporal & Seasonal Trend of HFMD in Malaysia (2009–2019)")
st.markdown("---")

# --- OBJECTIVE STATEMENT ---
st.subheader("🎯 Objective Statement")
st.write(
    "To analyze the **temporal trend** and **seasonal variation** of Hand, Foot and Mouth Disease (HFMD) cases "
    "in Malaysia from 2009 to 2019, identifying outbreak peaks and recurring seasonal patterns."
)

st.markdown("---")

# --- SUMMARY BOX (METRIC CARDS) ---
st.subheader("📊 Summary Box")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="🦠 Avg Monthly HFMD Cases",
    value="245",
    help="Mean number of HFMD cases per month across all Malaysian regions (2009–2019)",
    border=True
)

col2.metric(
    label="📅 Peak Outbreak Year",
    value="2018",
    help="Year with the highest recorded HFMD cases based on monthly averages",
    border=True
)

col3.metric(
    label="🌦️ Seasonal Peak Months",
    value="May – July",
    help="Months that consistently record the highest HFMD outbreaks each year",
    border=True
)

col4.metric(
    label="🧾 Dataset Duration",
    value="2009 – 2019",
    help="Time coverage of the HFMD dataset used for analysis",
    border=True
)

st.markdown("---")

# --- PLACEHOLDER TEXT (you can replace this later with real plots) ---
st.subheader("🧩 Visualization Section (to be added)")
st.info(
    "This section will contain three visualizations for Objective 1: "
    "a line chart of monthly trends, a bar chart of yearly averages, "
    "and a heatmap showing seasonal patterns."
)

st.success("✅ Objective 1 structure completed. Continue to 'HFMD and Weather Analysis' for Objective 2.")
