try:
    import streamlit as st
except ModuleNotFoundError:
    raise SystemExit("Streamlit is not installed. Ensure requirements.txt includes `streamlit==1.39.0`.")

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
col1.metric("🦠 Avg Monthly HFMD Cases", "245", help="Mean number per month (2009–2019).", border=True)
col2.metric("📅 Peak Outbreak Year", "2018", help="Highest average monthly HFMD cases.", border=True)
col3.metric("🌦️ Seasonal Peak Months", "May – July", help="Months with the most frequent peaks.", border=True)
col4.metric("🧾 Dataset Duration", "2009 – 2019", help="Temporal coverage of dataset.", border=True)
st.markdown("---")

# --- PLACEHOLDER TEXT ---
st.subheader("🧩 Visualization Section (to be added)")
st.info(
    "This section will contain three visualizations for Objective 1: "
    "a line chart of monthly trends, a bar chart of yearly averages, "
    "and a heatmap showing seasonal patterns."
)
st.success("✅ Objective 1 structure completed. Continue to 'HFMD and Weather Analysis' for Objective 2.")
