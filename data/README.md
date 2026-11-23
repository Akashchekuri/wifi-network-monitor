#  Wi-Fi Network Performance & Monitoring Dashboard

A real-time Wi-Fi network monitoring application built using Python and Streamlit. It monitors network connectivity, signal strength, latency, and packet loss, while providing an interactive dashboard for analyzing network performance.

##  Features

- Real-time Wi-Fi monitoring
- Internet connectivity detection
- Signal strength monitoring
- Network latency measurement
- Packet loss calculation
- Network health score (0–100)
- Automatic network alerts
- Network performance insights
- Historical performance analytics
- Interactive performance graphs
- Time-based data filtering
- CSV data export
- Automatic dashboard refresh

# Technologies Used

- Python
- Pandas
- Streamlit
- Plotly
- CSV
- Windows Networking Commands

##  Metrics Monitored

| Metric | Description |
|---|---|
| Signal Strength | Wi-Fi signal quality (%) |
| Latency | Network response time (ms) |
| Packet Loss | Percentage of lost packets |
| Internet Status | Connection status |
| Health Score | Overall network quality score |

##  Project Structure

```text
wifi-network/
│
├── data/
│   ├── network_data.csv
│   ├── dashboard.py
│   └── src/
│       └── monitor.py
│
└── README.md
```

##  Installation

Install the required packages:

```bash
pip install pandas streamlit plotly streamlit-autorefresh
```

## ▶ How to Run

### Step 1 — Start the Network Monitor

```bash
python .\data\src\monitor.py
```

### Step 2 — Start the Dashboard

Open another terminal:

```bash
streamlit run .\data\dashboard.py
```

### Step 3 — Open the Dashboard

Open the URL provided by Streamlit, usually:

```text
http://localhost:8501
```

##  Dashboard

The dashboard provides real-time monitoring, historical analytics, network health evaluation, and visual performance trends.

##  Project Objective

The objective of this project is to monitor Wi-Fi network performance in real time and help users identify connectivity problems, weak signal strength, high latency, and packet loss through a visual analytics dashboard.

##  Author

Akash Varma

B.Tech — Data Science