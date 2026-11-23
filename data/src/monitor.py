import subprocess
import platform
import re
import csv
import os
import time
from datetime import datetime


def get_wifi_info():

    result = subprocess.run(
        ["netsh", "wlan", "show", "interfaces"],
        capture_output=True,
        text=True
    )

    wifi_info = {}

    for line in result.stdout.splitlines():

        if "SSID" in line and "BSSID" not in line:
            wifi_info["SSID"] = line.split(":")[1].strip()

        elif "Signal" in line:
            wifi_info["Signal"] = line.split(":")[1].strip()

        elif "Channel" in line:
            wifi_info["Channel"] = line.split(":")[1].strip()

        elif "State" in line:
            wifi_info["State"] = line.split(":")[1].strip()

    return wifi_info


def check_internet():

    if platform.system() == "Windows":

        result = subprocess.run(
            ["ping", "-n", "4", "8.8.8.8"],
            capture_output=True,
            text=True
        )

    else:

        result = subprocess.run(
            ["ping", "-c", "4", "8.8.8.8"],
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
            metrics["Packet Loss"] = round((lost / sent) * 100, 2)

    latency_values = re.findall(r"time[=<](\d+)ms", output)

    latency_values = [int(value) for value in latency_values]

    if latency_values:

        metrics["Minimum Latency"] = min(latency_values)
        metrics["Maximum Latency"] = max(latency_values)

        metrics["Average Latency"] = round(
            sum(latency_values) / len(latency_values), 2
        )

    return metrics


def save_to_csv(data):

    # Get the project folder location
    project_folder = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )

    # Create the correct CSV path
    file_path = os.path.join(
        project_folder, "data", "network_data.csv"
    )

    # Create the folder if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Check if the CSV already exists
    file_exists = os.path.isfile(file_path)

    # Append data to CSV
    with open(file_path, "a", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=data.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)

    file_exists = os.path.isfile(file_path)

    with open(file_path, "a", newline="") as file:

        writer = csv.DictWriter(file, fieldnames=data.keys())

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

    while True:

        monitor_network()

        print("\nNext monitoring cycle in 10 seconds...")

        time.sleep(10)