import subprocess
import platform
import re
import csv
import time
from pathlib import Path
from datetime import datetime


def get_wifi_info():

    if platform.system() != "Windows":
        return {}

    result = subprocess.run(
        ["netsh", "wlan", "show", "interfaces"],
        capture_output=True,
        text=True
    )

    wifi_info = {}

    for line in result.stdout.splitlines():

        if "SSID" in line and "BSSID" not in line:
            wifi_info["SSID"] = line.split(":", 1)[1].strip()

        elif "Signal" in line:
            wifi_info["Signal"] = line.split(":", 1)[1].strip()

        elif "Channel" in line:
            wifi_info["Channel"] = line.split(":", 1)[1].strip()

        elif "State" in line:
            wifi_info["State"] = line.split(":", 1)[1].strip()

    return wifi_info


def check_internet():

    if platform.system() == "Windows":
        command = ["ping", "-n", "4", "8.8.8.8"]
    else:
        command = ["ping", "-c", "4", "8.8.8.8"]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return result.stdout


def extract_ping_metrics(output):

    metrics = {
        "Packets Sent": 0,
        "Packets Received": 0,
        "Packet Loss": 100,
        "Average Latency": None,
        "Minimum Latency": None,
        "Maximum Latency": None
    }

    packet_match = re.search(
        r"Sent = (\d+), Received = (\d+), Lost = (\d+)",
        output
    )

    if packet_match:

        sent = int(packet_match.group(1))
        received = int(packet_match.group(2))
        lost = int(packet_match.group(3))

        metrics["Packets Sent"] = sent
        metrics["Packets Received"] = received

        if sent > 0:
            metrics["Packet Loss"] = round(
                (lost / sent) * 100, 2
            )

    latency_values = re.findall(
        r"time[=<]\s*(\d+)\s*ms",
        output
    )

    latency_values = [int(value) for value in latency_values]

    if latency_values:

        metrics["Minimum Latency"] = min(latency_values)
        metrics["Maximum Latency"] = max(latency_values)

        metrics["Average Latency"] = round(
            sum(latency_values) / len(latency_values), 2
        )

    return metrics


def save_to_csv(data):

    # Get the main project directory
    project_folder = Path(__file__).resolve().parent.parent

    # CSV file location
    file_path = project_folder / "data" / "network_data.csv"

    # Create data folder if it does not exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_exists = file_path.exists() and file_path.stat().st_size > 0

    # Save data only once
    with open(file_path, "a", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=data.keys()
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)


def monitor_network():

    wifi_info = get_wifi_info()

    ping_output = check_internet()

    ping_metrics = extract_ping_metrics(ping_output)

    data = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "SSID": wifi_info.get("SSID"),
        "Signal": wifi_info.get("Signal"),
        "Channel": wifi_info.get("Channel"),
        "State": wifi_info.get("State"),
        **ping_metrics
    }

    save_to_csv(data)

    print("\n========== NETWORK MONITOR ==========")

    for key, value in data.items():
        print(f"{key}: {value}")

    print("\nData saved successfully!")


if __name__ == "__main__":

    print("Starting Wi-Fi monitoring...")
    print("Press CTRL+C to stop.\n")

    try:
        while True:

            monitor_network()

            print("\nNext monitoring cycle in 10 seconds...")

            time.sleep(10)

    except KeyboardInterrupt:
        print("\nWi-Fi monitoring stopped.")