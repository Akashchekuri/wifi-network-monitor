import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from streamlit_autorefresh import st_autorefresh

# Dashboard configuration
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
# Automatically refresh dashboard every 5 seconds
st_autorefresh(interval=5000, key="wifi_refresh")
# Project paths
PROJECT_DIR = Path(__file__).parent
CSV_PATH = PROJECT_DIR /  "network_data.csv"

# Dashboard title
st.title("📶 Wi-Fi Network Performance Dashboard")
st.caption("Real-time monitoring of your Wi-Fi network")

# Refresh button
if st.button("🔄 Refresh Data"):
    st.rerun()

# Load CSV data
if not CSV_PATH.exists():
    st.error(f"Data file not found: {CSV_PATH}")
    st.stop()

df = pd.read_csv(CSV_PATH)

if df.empty:
    st.warning("No network data available yet.")
    st.stop()

# Clean column names
df.columns = df.columns.str.strip()

# Convert timestamp to datetime
if "Timestamp" in df.columns:
    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"], errors="coerce"
    )

#
# Time Filter
st.subheader("🕒 Filter Data by Time")

time_filter = st.selectbox(
    "Select Time Range",
    ["All Data", "Last 15 Minutes", "Last 1 Hour", "Last 6 Hours"]
)

current_time = pd.Timestamp.now()

if time_filter == "Last 15 Minutes":
    df = df[df["Timestamp"] >= current_time - pd.Timedelta(minutes=15)]

elif time_filter == "Last 1 Hour":
    df = df[df["Timestamp"] >= current_time - pd.Timedelta(hours=1)]

elif time_filter == "Last 6 Hours":
    df = df[df["Timestamp"] >= current_time - pd.Timedelta(hours=6)]

if df.empty:
    st.warning("No data available for the selected time range.")
    st.stop()

# Latest record
latest = df.iloc[-1]
# Convert metrics to numeric values
signal = pd.to_numeric(latest.get("Signal"), errors="coerce")
latency = pd.to_numeric(latest.get("Average Latency"), errors="coerce")
loss = pd.to_numeric(latest.get("Packet Loss"), errors="coerce")

# Metrics
st.subheader("Current Network Status")

col1, col2, col3, col4 = st.columns(4)

with col1:
    state = latest.get("State", "Unknown")
    st.metric("Internet Status", str(state))

with col2:
    signal = pd.to_numeric(latest.get("Signal"), errors="coerce")
    st.metric(
        "Signal Strength",
        f"{signal}%" if pd.notna(signal) else "N/A"
    )

with col3:
    latency = pd.to_numeric(latest.get("Average Latency"), errors="coerce")
    st.metric(
        "Average Latency",
        f"{latency} ms" if pd.notna(latency) else "N/A"
    )

with col4:
    loss = pd.to_numeric(latest.get("Packet Loss"), errors="coerce")
    st.metric(
        "Packet Loss",
        f"{loss}%" if pd.notna(loss) else "N/A"
    )
# Network Health Score

score = 100

if pd.notna(latency):
    if latency > 200:
        score -= 40
    elif latency > 100:
        score -= 25
    elif latency > 50:
        score -= 10

if pd.notna(loss):
    if loss > 20:
        score -= 40
    elif loss > 10:
        score -= 25
    elif loss > 0:
        score -= 15

if pd.notna(signal):
    if signal < 30:
        score -= 30
    elif signal < 50:
        score -= 20
    elif signal < 80:
        score -= 10

score = max(0, score)

st.subheader("🩺 Network Health")

col1, col2 = st.columns(2)

with col1:
    st.metric("Health Score", f"{score}/100")
    # Network Health Gauge

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

st.plotly_chart(gauge, use_container_width=True)

with col2:
    if score >= 80:
        st.success("Excellent Network 🟢")
    elif score >= 60:
        st.info("Good Network 🔵")
    elif score >= 40:
        st.warning("Fair Network 🟡")
    else:
        st.error("Poor Network 🔴")
# Network Alerts
# Network Performance Insights

st.subheader("💡 Network Performance Insights")

if pd.notna(latency):
    if latency < 50:
        st.write("🟢 Latency is excellent. Your connection is responsive.")
    elif latency < 100:
        st.write("🟡 Latency is acceptable for normal usage.")
    else:
        st.write("🔴 High latency may affect gaming and video calls.")

if pd.notna(signal):
    if signal >= 80:
        st.write("🟢 Wi-Fi signal is strong.")
    elif signal >= 50:
        st.write("🟡 Wi-Fi signal is moderate. Moving closer to the router may help.")
    else:
        st.write("🔴 Wi-Fi signal is weak. Try moving closer to your router.")

if pd.notna(loss):
    if loss == 0:
        st.write("🟢 No packet loss detected.")
    else:
        st.write(f"⚠️ Packet loss detected: {loss}%.")
st.subheader("🚨 Network Alerts")

if state != "connected":
    st.error("🔴 Internet connection may be disconnected!")

if pd.notna(latency) and latency > 100:
    st.warning("⚠️ High latency detected!")

if pd.notna(loss) and loss > 5:
    st.warning("⚠️ High packet loss detected!")

if pd.notna(signal) and signal < 50:
    st.warning("📶 Weak Wi-Fi signal!")

if (
    state == "connected"
    and (pd.isna(latency) or latency <= 100)
    and (pd.isna(loss) or loss <= 5)
    and (pd.isna(signal) or signal >= 50)
):
    st.success("✅ Your network is performing normally.")# Additional network information
st.subheader("Network Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("**Wi-Fi Name (SSID)**")
    st.write(latest.get("SSID", "Unknown"))

with col2:
    st.write("**Wi-Fi Channel**")
    st.write(latest.get("Channel", "Unknown"))

with col3:
    st.write("**Connection State**")
    st.write(latest.get("State", "Unknown"))

# Historical Analytics
# Historical Analytics
st.subheader("📊 Historical Analytics")

# Convert columns to numeric before calculations
df["Average Latency"] = pd.to_numeric(
    df["Average Latency"], errors="coerce"
)

df["Signal"] = pd.to_numeric(
    df["Signal"], errors="coerce"
)

df["Packet Loss"] = pd.to_numeric(
    df["Packet Loss"], errors="coerce"
)

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
# Network Performance Graphs

st.subheader("📊 Network Performance Trends")

col1, col2 = st.columns(2)

# Latency Graph
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

    st.plotly_chart(fig_latency, use_container_width=True)


# Signal Strength Graph
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

    st.plotly_chart(fig_signal, use_container_width=True)


# Packet Loss Graph

# Packet Loss Graph
st.subheader("📉 Packet Loss History")

if "Packet Loss" in df.columns:

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

    st.plotly_chart(fig_loss, use_container_width=True)
    

# Download Network Data
st.subheader("📥 Download Network Data")

csv_download = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Network Data CSV",
    data=csv_download,
    file_name="wifi_network_report.csv",
    mime="text/csv"
)# Network data table
st.subheader("📋 Recorded Network Data")

st.dataframe(
    df.tail(20),
    use_container_width=True
)

# Footer
st.caption("Wi-Fi Network Monitoring System | Built using Python")