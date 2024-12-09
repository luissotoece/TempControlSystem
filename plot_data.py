# plot_data.py

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import time

# Path to the CSV file
csv_file = 'historian_data.csv'

def plot_temperature():
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Convert Timestamp column to datetime objects
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Plot Temperature over Time
    plt.figure(figsize=(12, 6))
    plt.plot(df['Timestamp'], df['Temperature (°C)'], marker='o', linestyle='-')
    plt.title('Temperature Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.gcf().autofmt_xdate()  # Auto-format the x-axis labels for dates

    # Show the plot
    plt.tight_layout()
    plt.show()

def plot_system_status():
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Convert Timestamp column to datetime objects
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Map System Status to numerical values
    df['System Status Numeric'] = df['System Status'].map({'Running': 1, 'Stopped': 0})

    # Plot System Status over Time
    plt.figure(figsize=(12, 4))
    plt.step(df['Timestamp'], df['System Status Numeric'], where='post')
    plt.title('System Status Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('System Status (1=Running, 0=Stopped)')
    plt.yticks([0, 1], ['Stopped', 'Running'])
    plt.grid(True)
    plt.gcf().autofmt_xdate()

    # Show the plot
    plt.tight_layout()
    plt.show()

def plot_live():
    # Initial empty DataFrame
    df = pd.DataFrame()

    print("Press Ctrl+C to stop live plotting.")
    try:
        while True:
            # Read the CSV file
            df = pd.read_csv(csv_file)

            # Convert Timestamp column to datetime objects
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])

            # Plot Temperature and System Status
            plt.figure(figsize=(12, 10))

            # Subplot 1: Temperature
            plt.subplot(2, 1, 1)
            plt.plot(df['Timestamp'], df['Temperature (°C)'], marker='o', linestyle='-')
            plt.title('Temperature Over Time')
            plt.xlabel('Timestamp')
            plt.ylabel('Temperature (°C)')
            plt.grid(True)
            plt.gcf().autofmt_xdate()

            # Subplot 2: System Status
            plt.subplot(2, 1, 2)
            df['System Status Numeric'] = df['System Status'].map({'Running': 1, 'Stopped': 0})
            plt.step(df['Timestamp'], df['System Status Numeric'], where='post')
            plt.title('System Status Over Time')
            plt.xlabel('Timestamp')
            plt.ylabel('System Status')
            plt.yticks([0, 1], ['Stopped', 'Running'])
            plt.grid(True)
            plt.gcf().autofmt_xdate()

            # Adjust layout and display
            plt.tight_layout()
            plt.pause(1)
            plt.clf()  # Clear the figure for the next loop

            time.sleep(1)  # Wait for a second before updating

    except KeyboardInterrupt:
        print("Live plotting stopped.")

if __name__ == '__main__':
    print("Choose an option:")
    print("1. Plot Temperature Over Time")
    print("2. Plot System Status Over Time")
    print("3. Live Plot (Temperature and System Status)")
    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        plot_temperature()
    elif choice == '2':
        plot_system_status()
    elif choice == '3':
        plot_live()
    else:
        print("Invalid choice.")