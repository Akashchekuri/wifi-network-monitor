# Wi-Fi Network Performance & Monitoring Dashboard

A real-time Wi-Fi network monitoring application built using Python, Pandas, Streamlit, and Plotly. It collects network performance data, monitors Wi-Fi connectivity, measures latency and packet loss, and presents the results through an interactive dashboard.

## Features

- Real-time Wi-Fi monitoring
- Internet connectivity detection
- Wi-Fi signal strength monitoring
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

## Technologies Used

- Python
- Pandas
- Streamlit
- Plotly
- CSV
- Windows Networking Commands

## Metrics Monitored

| Metric | Description |
|---|---|
| Signal Strength | Wi-Fi signal quality (%) |
| Latency | Network response time (ms) |
| Packet Loss | Percentage of lost packets |
| Internet Status | Network connectivity status |
| Health Score | Overall network performance score |

## Project Structure

```text
wifi-network-monitor/
│
├── data/
│   └── network_data.csv
│
├── src/
│   └── monitor.py
│
├── dashboard.py
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Akashchekuri/wifi-network-monitor.git
```

### 2. Navigate to the Project Folder

```bash
cd wifi-network-monitor
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## How to Run

### Step 1 — Start the Network Monitor

```bash
python src/monitor.py
```

The monitoring system collects Wi-Fi information and network performance metrics every 10 seconds and stores the results in a CSV file.

### Step 2 — Start the Dashboard

Open another terminal in the project folder and execute:

```bash
streamlit run dashboard.py
```

### Step 3 — Open the Dashboard

Open the local URL provided by Streamlit:

```text
http://localhost:8501
```

## Dashboard

The interactive dashboard provides:

- Current network performance metrics
- Network health score
- Connectivity alerts and insights
- Historical performance analytics
- Latency, signal strength, and packet loss graphs
- Time-based performance filtering
- CSV data export

## Project Objective

The objective of this project is to monitor Wi-Fi network performance, identify connectivity issues, analyze network quality, and visualize performance trends through an interactive dashboard.

## Author

**Akash Varma**

B.Tech — Data Science