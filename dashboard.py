import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from streamlit_autorefresh import st_autorefresh


# ==========================================
# 1. DASHBOARD CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Wi-Fi Network Monitor",
    page_icon="📶",
    layout="wide"
)

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stMetric"] {
    background-color: #111827;
    border: 1px solid #374151;
    padding: 20px;
    border-radius: 15px;
}

[data-testid="stMetricLabel"] {
    color: #9CA3AF;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF;
}

h1 {
    color: #38BDF8;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. AUTOMATIC REFRESH
# ==========================================

st_autorefresh(
    interval=5000,
    key="wifi_refresh"
)


# ==========================================
# 3. PROJECT PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent

CSV_PATH = PROJECT_DIR / "data" / "network_data.csv"


# ==========================================
# 4. DASHBOARD HEADER
# ==========================================

st.title("📶 Wi-Fi Network Performance Dashboard")

st.caption("Real-time monitoring of your Wi-Fi network")

if st.button("🔄 Refresh Data"):
    st.rerun()


# ==========================================
# 5. LOAD NETWORK DATA
# ==========================================

if not CSV_PATH.exists():

    st.error(f"Data file not found: {CSV_PATH}")
    st.stop()

try:
    df = pd.read_csv(CSV_PATH)

except Exception as error:

    st.error(f"Unable to read network data: {error}")
    st.stop()


if df.empty:

    st.warning("No network data available yet.")
    st.stop()


# Clean column names
df.columns = df.columns.str.strip()


# Required columns
required_columns = [
    "Timestamp",
    "SSID",
    "Signal",
    "Channel",
    "State",
    "Packets Sent",
    "Packets Received",
    "Packet Loss",
    "Average Latency",
    "Minimum Latency",
    "Maximum Latency"
]

for column in required_columns:

    if column not in df.columns:
        df[column] = None


# Convert timestamp
df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)

# Remove records without valid timestamps
df = df.dropna(subset=["Timestamp"])

if df.empty:

    st.warning("No valid timestamp records found.")
    st.stop()


# Convert numeric columns
numeric_columns = [
    "Signal",
    "Packets Sent",
    "Packets Received",
    "Packet Loss",
    "Average Latency",
    "Minimum Latency",
    "Maximum Latency"
]

for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column].astype(str).str.replace("%", "", regex=False),
        errors="coerce"
    )


# ==========================================
# 6. TIME FILTER
# ==========================================

st.subheader("🕒 Filter Data by Time")

time_filter = st.selectbox(
    "Select Time Range",
    [
        "All Data",
        "Last 15 Minutes",
        "Last 1 Hour",
        "Last 6 Hours"
    ]
)

current_time = pd.Timestamp.now()

if time_filter == "Last 15 Minutes":

    df = df[
        df["Timestamp"] >= current_time - pd.Timedelta(minutes=15)
    ]

elif time_filter == "Last 1 Hour":

    df = df[
        df["Timestamp"] >= current_time - pd.Timedelta(hours=1)
    ]

elif time_filter == "Last 6 Hours":

    df = df[
        df["Timestamp"] >= current_time - pd.Timedelta(hours=6)
    ]


if df.empty:

    st.warning("No data available for the selected time range.")
    st.stop()


# Sort records by timestamp
df = df.sort_values("Timestamp")

# Latest record
latest = df.iloc[-1]


# ==========================================
# 7. CURRENT NETWORK STATUS
# ==========================================

st.subheader("📡 Current Network Status")


state = str(latest.get("State", "Unknown")).strip()

state_normalized = state.lower()

signal = latest["Signal"]
latency = latest["Average Latency"]
loss = latest["Packet Loss"]


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Internet Status",
        state.capitalize() if state else "Unknown"
    )


with col2:

    st.metric(
        "Signal Strength",
        f"{signal:.0f}%" if pd.notna(signal) else "N/A"
    )


with col3:

    st.metric(
        "Average Latency",
        f"{latency:.2f} ms" if pd.notna(latency) else "N/A"
    )


with col4:

    st.metric(
        "Packet Loss",
        f"{loss:.2f}%" if pd.notna(loss) else "N/A"
    )


# ==========================================
# 8. NETWORK HEALTH SCORE
# ==========================================

score = 100


# Latency calculation
if pd.notna(latency):

    if latency > 200:
        score -= 40

    elif latency > 100:
        score -= 25

    elif latency > 50:
        score -= 10


# Packet loss calculation
if pd.notna(loss):

    if loss > 20:
        score -= 40

    elif loss > 10:
        score -= 25

    elif loss > 0:
        score -= 15


# Signal strength calculation
if pd.notna(signal):

    if signal < 30:
        score -= 30

    elif signal < 50:
        score -= 20

    elif signal < 80:
        score -= 10


# Internet connectivity calculation
if state_normalized != "connected":
    score -= 40


score = max(0, min(100, score))


# ==========================================
# 9. NETWORK HEALTH VISUALIZATION
# ==========================================

st.subheader("🩺 Network Health")

col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Network Health Score",
        f"{score}/100"
    )


    gauge = px.pie(
        values=[score, 100 - score],
        names=["Health", "Remaining"],
        hole=0.7,
        title="Network Health"
    )

    gauge.update_traces(
        textinfo="none",
        hoverinfo="skip"
    )

    gauge.update_layout(
        showlegend=False,
        annotations=[
            dict(
                text=f"{score}/100",
                x=0.5,
                y=0.5,
                font_size=30,
                showarrow=False
            )
        ]
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )


with col2:

    if score >= 80:

        st.success("Excellent Network 🟢")

    elif score >= 60:

        st.info("Good Network 🔵")

    elif score >= 40:

        st.warning("Fair Network 🟡")

    else:

        st.error("Poor Network 🔴")


# ==========================================
# 10. NETWORK PERFORMANCE INSIGHTS
# ==========================================

st.subheader("💡 Network Performance Insights")


if pd.notna(latency):

    if latency < 50:

        st.write(
            "🟢 Latency is excellent. Your connection is responsive."
        )

    elif latency < 100:

        st.write(
            "🟡 Latency is acceptable for normal usage."
        )

    else:

        st.write(
            "🔴 High latency may affect gaming and video calls."
        )


if pd.notna(signal):

    if signal >= 80:

        st.write("🟢 Wi-Fi signal is strong.")

    elif signal >= 50:

        st.write(
            "🟡 Wi-Fi signal is moderate. Moving closer to the router may help."
        )

    else:

        st.write(
            "🔴 Wi-Fi signal is weak. Try moving closer to your router."
        )


if pd.notna(loss):

    if loss == 0:

        st.write("🟢 No packet loss detected.")

    else:

        st.write(f"⚠️ Packet loss detected: {loss}%.")


# ==========================================
# 11. NETWORK ALERTS
# ==========================================

st.subheader("🚨 Network Alerts")

if state_normalized != "connected":

    st.error("🔴 Internet connection may be disconnected!")


if pd.notna(latency) and latency > 100:

    st.warning("⚠️ High latency detected!")


if pd.notna(loss) and loss > 5:

    st.warning("⚠️ High packet loss detected!")


if pd.notna(signal) and signal < 50:

    st.warning("📶 Weak Wi-Fi signal!")


if (
    state_normalized == "connected"
    and (pd.isna(latency) or latency <= 100)
    and (pd.isna(loss) or loss <= 5)
    and (pd.isna(signal) or signal >= 50)
):

    st.success("✅ Your network is performing normally.")


# ==========================================
# 12. NETWORK INFORMATION
# ==========================================

st.subheader("🌐 Network Information")

col1, col2, col3 = st.columns(3)


with col1:

    st.write("**Wi-Fi Name (SSID)**")

    st.write(latest.get("SSID", "Unknown"))


with col2:

    st.write("**Wi-Fi Channel**")

    st.write(latest.get("Channel", "Unknown"))


with col3:

    st.write("**Connection State**")

    st.write(state)


# ==========================================
# 13. HISTORICAL ANALYTICS
# ==========================================

st.subheader("📊 Historical Analytics")


col1, col2, col3, col4 = st.columns(4)


with col1:

    avg_latency_history = df["Average Latency"].mean()

    st.metric(
        "Historical Average Latency",
        f"{avg_latency_history:.2f} ms"
        if pd.notna(avg_latency_history)
        else "N/A"
    )


with col2:

    max_latency_history = df["Average Latency"].max()

    st.metric(
        "Maximum Latency Recorded",
        f"{max_latency_history:.2f} ms"
        if pd.notna(max_latency_history)
        else "N/A"
    )


with col3:

    avg_signal_history = df["Signal"].mean()

    st.metric(
        "Historical Average Signal",
        f"{avg_signal_history:.2f}%"
        if pd.notna(avg_signal_history)
        else "N/A"
    )


with col4:

    avg_loss_history = df["Packet Loss"].mean()

    st.metric(
        "Average Packet Loss",
        f"{avg_loss_history:.2f}%"
        if pd.notna(avg_loss_history)
        else "N/A"
    )


# ==========================================
# 14. NETWORK PERFORMANCE GRAPHS
# ==========================================

st.subheader("📈 Network Performance Trends")

col1, col2 = st.columns(2)


# Latency graph
with col1:

    fig_latency = px.line(
        df,
        x="Timestamp",
        y="Average Latency",
        title="Latency Over Time",
        markers=True
    )

    fig_latency.update_layout(
        xaxis_title="Time",
        yaxis_title="Latency (ms)"
    )

    st.plotly_chart(
        fig_latency,
        use_container_width=True
    )


# Signal graph
with col2:

    fig_signal = px.line(
        df,
        x="Timestamp",
        y="Signal",
        title="Signal Strength Over Time",
        markers=True
    )

    fig_signal.update_layout(
        xaxis_title="Time",
        yaxis_title="Signal (%)"
    )

    st.plotly_chart(
        fig_signal,
        use_container_width=True
    )


# ==========================================
# 15. PACKET LOSS GRAPH
# ==========================================

st.subheader("📉 Packet Loss History")


fig_loss = px.line(
    df,
    x="Timestamp",
    y="Packet Loss",
    title="Packet Loss Over Time",
    markers=True
)

fig_loss.update_layout(
    xaxis_title="Time",
    yaxis_title="Packet Loss (%)"
)

st.plotly_chart(
    fig_loss,
    use_container_width=True
)


# ==========================================
# 16. DOWNLOAD NETWORK DATA
# ==========================================

st.subheader("📥 Download Network Data")

csv_download = df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇️ Download Network Data CSV",
    data=csv_download,
    file_name="wifi_network_report.csv",
    mime="text/csv"
)


# ==========================================
# 17. RECORDED NETWORK DATA
# ==========================================

st.subheader("📋 Recorded Network Data")

st.dataframe(
    df.tail(20),
    use_container_width=True
)


# ==========================================
# 18. FOOTER
# ==========================================

st.caption(
    "Wi-Fi Network Monitoring System | Built using Python, Pandas, Streamlit and Plotly"
)