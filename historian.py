# historian.py

import csv
import time
from datetime import datetime
from pymodbus.client import ModbusTcpClient

# PLC Configuration
PLC_IP = 'localhost'
PLC_PORT = 5020  # Should match the port in modbus_server.py

# Connect to the PLC
client = ModbusTcpClient(PLC_IP, port=PLC_PORT)

# Check connection
if not client.connect():
    print("Unable to connect to PLC.")
    exit()

# CSV file setup
csv_file = 'historian_data.csv'
fieldnames = [
    'Timestamp', 'Temperature (°C)', 'Humidity (%)', 'Setpoint (°C)',
    'System Status', 'Overheat Alarm', 'Door Status'
]

# Create the CSV file and write the header
with open(csv_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

# Function to read data from PLC and write to CSV
def collect_data():
    while True:
        try:
            # Read data from PLC
            temp_response = client.read_holding_registers(1, 1)  # Temp_Sensor
            humidity_response = client.read_holding_registers(2, 1)  # Humidity_Sensor
            setpoint_response = client.read_holding_registers(0, 1)  # Temp_Setpoint
            system_enable_response = client.read_coils(2, 1)  # System_Enable
            overheat_alarm_response = client.read_discrete_inputs(1, 1)  # Overheat_Alarm
            door_status_response = client.read_discrete_inputs(0, 1)  # Door_Sensor

            # Process responses
            if not temp_response.isError():
                temperature = temp_response.registers[0]
            else:
                temperature = 'Error'

            if not humidity_response.isError():
                humidity = humidity_response.registers[0]
            else:
                humidity = 'Error'

            if not setpoint_response.isError():
                setpoint = setpoint_response.registers[0]
            else:
                setpoint = 'Error'

            if not system_enable_response.isError():
                system_enable = system_enable_response.bits[0]
                system_status = 'Running' if system_enable else 'Stopped'
            else:
                system_status = 'Error'

            if not overheat_alarm_response.isError():
                overheat_alarm = overheat_alarm_response.bits[0]
                overheat_status = 'Active' if overheat_alarm else 'Inactive'
            else:
                overheat_status = 'Error'

            if not door_status_response.isError():
                door_open = door_status_response.bits[0]
                door_status = 'Open' if door_open else 'Closed'
            else:
                door_status = 'Error'

            # Get current timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Write data to CSV
            with open(csv_file, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerow({
                    'Timestamp': timestamp,
                    'Temperature (°C)': temperature,
                    'Humidity (%)': humidity,
                    'Setpoint (°C)': setpoint,
                    'System Status': system_status,
                    'Overheat Alarm': overheat_status,
                    'Door Status': door_status
                })

            print(f"Data logged at {timestamp}")
            time.sleep(1)

        except Exception as e:
            print(f"Error collecting data: {e}")
            time.sleep(1)

if __name__ == '__main__':
    try:
        collect_data()
    except KeyboardInterrupt:
        print("Historian stopped by user.")
        client.close()