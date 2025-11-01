import streamlit as st
import pandas as pd

# ------------------ TITLE & OBJECTIVE ------------------
st.title("🦠 Objective 1: HFMD Temporal & Seasonal Trend (2009–2019)")
st.markdown("---")

st.subheader("🎯 Objective Statement")
st.write(
    "Analyze the **temporal trend** and **seasonal variation** of HFMD cases in Malaysia (2009–2019) "
    "to identify outbreak peaks and recurring seasonal patterns."
)
st.markdown("---")

import time

DATA_URL = "https://raw.githubusercontent.com/AleyaNazifa/AssignmentSV2025-1/refs/heads/main/hfdm_data%20-%20Upload.csv"

@st.cache_data(show_spinner=False)
def load_raw(url: str) -> pd.DataFrame:
    df = pd.read_csv(url)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

with st.status("Loading & validating dataset…", expanded=False) as s:
    try:
        df_raw = load_raw(DATA_URL)
        time.sleep(0.2)  # just to let the status animate
        s.update(label="Parsing dates…")

        if "date" not in df_raw.columns:
            st.error("❌ CSV must contain a 'Date' column.")
            st.stop()

        df_raw["date"] = pd.to_datetime(df_raw["date"], format="%d/%m/%Y", errors="coerce")
        df_raw = df_raw.dropna(subset=["date"]).sort_values("date")

        regions = ["southern", "northern", "central", "east_coast", "borneo"]
        missing = [c for c in regions if c not in df_raw.columns]
        if missing:
            st.error(f"❌ Missing region columns: {missing}")
            st.stop()

        df_raw["total_cases"] = df_raw[regions].sum(axis=1, numeric_only=True)

        s.update(label="Aggregating monthly…")
        df_m = (
            df_raw.set_index("date")
                  .resample("M")
                  .mean(numeric_only=True)
                  .reset_index()
                  .rename(columns={"date": "Date"})
        )
        df_m["Year"] = df_m["Date"].dt.year
        df_m["Month"] = df_m["Date"].dt.month

        if df_m.empty or df_m["total_cases"].isna().all():
            st.error("❌ Monthly data is empty. Check if the CSV has numeric case values for regions.")
            st.stop()

        s.update(state="complete", label="✅ Data ready")

    except Exception as e:
        s.update(state="error", label="❌ Failed to load data")
        st.error(f"Error: {e}")
        st.stop()

with st.expander("🔎 Debug: data status", expanded=False):
    st.write("**Columns:**", list(df_raw.columns))
    st.write("**Date range:**", df_raw["date"].min(), "→", df_raw["date"].max())
    st.write("**Rows (raw / monthly):**", len(df_raw), "/", len(df_m))
    st.dataframe(df_m.head(), use_container_width=True)


# ------------------ SUMMARY BOX (3 METRICS, DYNAMIC) ------------------
avg_monthly = df_m["total_cases"].mean()
peak_year   = df_m.groupby("Year")["total_cases"].mean().idxmax()
top_months  = (df_m.groupby("Month")["total_cases"].mean()
               .sort_values(ascending=False).head(3).index.tolist())
month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
seasonal_peak = " – ".join(month_names[m-1] for m in sorted(top_months))

st.subheader("📊 Summary Box")
c1, c2, c3 = st.columns(3)
c1.metric("📈 Avg Monthly HFMD Cases", f"{avg_monthly:.0f}",
          help="Mean monthly HFMD cases across all regions (2009–2019).", border=True)
c2.metric("📅 Peak Outbreak Year", f"{int(peak_year)}",
          help="Year with the highest average monthly cases.", border=True)
c3.metric("🌦️ Seasonal Peak Months", seasonal_peak,
          help="Months with most frequent surges.", border=True)
st.markdown("---")

# ------------------ DATA PREVIEW ------------------
st.header("1) Data Preview (Monthly)")
st.dataframe(df_m.head(), use_container_width=True)
st.caption(f"Rows: {len(df_m):,} • Years: {df_m['Year'].min()}–{df_m['Year'].max()}")
st.markdown("---")

# ------------------ VIZ 1: LINE (Streamlit built-in) ------------------
st.header("2) Monthly HFMD Cases Trend")
line_df = df_m[["Date", "total_cases"]].set_index("Date")
st.line_chart(line_df, height=350)
st.info("**Interpretation:** Clear **mid-year peaks** recur almost every year — strong seasonal signal.")
st.markdown("---")

# ------------------ VIZ 2: YEARLY BAR (Streamlit built-in) ------------------
st.header("3) Average Yearly HFMD Cases")
yearly = df_m.groupby("Year", as_index=False)["total_cases"].mean().rename(
    columns={"total_cases": "AvgMonthlyCases"}
)
yearly_chart = yearly.set_index("Year")
st.bar_chart(yearly_chart, height=350)
st.info("**Interpretation:** Some years show **higher baseline incidence**, useful for long-term planning.")
st.markdown("---")

# ------------------ VIZ 3: HEATMAP (Vega-Lite spec, no extra libs) ------------------
st.header("4) Seasonal Pattern (Month × Year Heatmap)")

# long format for Vega-Lite
heat_df = df_m[["Year","Month","total_cases"]].rename(columns={"total_cases":"AvgMonthlyCases"})
st.vega_lite_chart(
    heat_df,
    {
        "mark": "rect",
        "encoding": {
            "x": {"field": "Year", "type": "ordinal", "title": "Year"},
            "y": {"field": "Month", "type": "ordinal",
                  "title": "Month",
                  "scale": {"domain": list(range(1,13))},
                  "axis": {"labelExpr":
                      "['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][datum.value-1]"}
                 },
            "color": {"field": "AvgMonthlyCases", "type": "quantitative", "title": "Avg Monthly Cases",
                      "scale": {"scheme": "yelloworangered"}}
        },
        "width": "container",
        "height": 340,
        "config": {"axis": {"labelFontSize": 12, "titleFontSize": 12}}
    },
    use_container_width=True
)
st.info("**Interpretation:** Heatmap confirms **recurring mid-year surges**; intensity varies year-to-year.")
st.success("✅ Objective 1 complete: 3 visuals rendered (no external plotting libraries).")
