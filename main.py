from src.monitor import monitor_network


def main():

    print("\n========== WIFI NETWORK MONITOR ==========")
    print("Starting network monitoring...\n")

    try:
        monitor_network()

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

    except Exception as error:
        print(f"\nAn error occurred: {error}")


if __name__ == "__main__":
    main()