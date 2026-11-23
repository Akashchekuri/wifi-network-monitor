import subprocess
import platform
import re


def get_wifi_info():

    result = subprocess.run(
        ["netsh", "wlan", "show", "interfaces"],
        capture_output=True,
        text=True
    )

    output = result.stdout

    wifi_info = {}

    for line in output.splitlines():

        if "SSID" in line and "BSSID" not in line:
            wifi_info["SSID"] = line.split(":")[1].strip()

        elif "Signal" in line:
            wifi_info["Signal"] = line.split(":")[1].strip()

        elif "Channel" in line:
            wifi_info["Channel"] = line.split(":")[1].strip()

        elif "State" in line:
            wifi_info["State"] = line.split(":")[1].strip()

        elif "Radio type" in line:
            wifi_info["Radio type"] = line.split(":")[1].strip()

    return wifi_info


def check_internet():

    system = platform.system()

    if system == "Windows":

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

    output = result.stdout

    if result.returncode == 0:
        status = "Connected"
    else:
        status = "Disconnected"

    return status, output


def extract_ping_metrics(output):

    metrics = {}

    # Extract packets sent, received, and lost
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
        metrics["Packets Lost"] = lost

        if sent > 0:
            packet_loss = (lost / sent) * 100
        else:
            packet_loss = 0

        metrics["Packet Loss"] = round(packet_loss, 2)

    # Extract latency values
    latency_values = re.findall(
        r"time[=<](\d+)ms",
        output
    )

    latency_values = [int(value) for value in latency_values]

    if latency_values:

        metrics["Minimum Latency"] = min(latency_values)
        metrics["Maximum Latency"] = max(latency_values)

        metrics["Average Latency"] = round(
            sum(latency_values) / len(latency_values),
            2
        )

    else:

        metrics["Minimum Latency"] = None
        metrics["Maximum Latency"] = None
        metrics["Average Latency"] = None

    return metrics


# Collect Wi-Fi information
wifi_data = get_wifi_info()

# Test internet connectivity
internet_status, ping_output = check_internet()

# Extract performance metrics
ping_metrics = extract_ping_metrics(ping_output)


# Display results
print("\n========== WIFI MONITOR ==========")

print("\n--- Wi-Fi Details ---")

for key, value in wifi_data.items():
    print(f"{key}: {value}")


print("\n--- Internet Status ---")

print(f"Internet: {internet_status}")


print("\n--- Network Performance ---")

for key, value in ping_metrics.items():
    print(f"{key}: {value}")