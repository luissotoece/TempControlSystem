# # hmi_app.py

# import tkinter as tk
# from tkinter import ttk, messagebox
# from pymodbus.client import ModbusTcpClient
# import threading
# import time

# # PLC Configuration
# PLC_IP = 'localhost'  # Connect to the local Modbus server
# PLC_PORT = 5020       # Port number matching the server script

# # Connect to the PLC
# client = ModbusTcpClient(PLC_IP, port=PLC_PORT)

# # Check connection
# if not client.connect():
#     messagebox.showerror("Connection Error", "Unable to connect to PLC.")
#     exit()

# # Create the main application window
# root = tk.Tk()
# root.title("Temperature Control System HMI")
# root.geometry("800x600")

# # Variables for holding values
# setpoint_var = tk.DoubleVar()
# current_temp_var = tk.StringVar(value="--")
# current_humidity_var = tk.StringVar(value="--")
# system_status_var = tk.StringVar(value="Stopped")
# door_status_var = tk.StringVar(value="Closed")
# overheat_alarm_var = tk.StringVar(value="")

# # Function to send start/stop command to the PLC
# def send_start_stop_command(start):
#     client.write_coil(0, start)  # Coil 0: Start_Stop_Button
#     # System_Enable is updated by PLC logic; we'll read it in update_values()

# # Function to send emergency stop command
# def send_emergency_stop():
#     client.write_coil(1, False)  # Coil 1: Safety_Switch (set to False to stop)
#     messagebox.showwarning("Emergency Stop", "Emergency Stop Activated!")

# # Function to update setpoint temperature
# def update_setpoint(value):
#     client.write_register(0, int(float(value)))  # Register 0: Temp_Setpoint

# # Function to update displayed values
# def update_values():
#     while True:
#         try:
#             # Read current temperature and humidity from PLC
#             temp_response = client.read_holding_registers(1, 1)  # Register 1: Temp_Sensor
#             humidity_response = client.read_holding_registers(2, 1)  # Register 2: Humidity_Sensor

#             if not temp_response.isError():
#                 current_temp = temp_response.registers[0]
#                 current_temp_var.set(f"{current_temp} °C")
#             else:
#                 current_temp_var.set("Error")

#             if not humidity_response.isError():
#                 current_humidity = humidity_response.registers[0]
#                 current_humidity_var.set(f"{current_humidity} %")
#             else:
#                 current_humidity_var.set("Error")

#             # Read system status and indicators
#             system_enable_response = client.read_coils(2, 1)  # Coil 2: System_Enable
#             door_status_response = client.read_discrete_inputs(0, 1)  # Input 0: Door_Sensor
#             overheat_alarm_response = client.read_discrete_inputs(1, 1)  # Input 1: Overheat_Alarm

#             if not system_enable_response.isError():
#                 system_enable = system_enable_response.bits[0]
#                 status = "Running" if system_enable else "Stopped"
#                 system_status_var.set(status)
#             else:
#                 system_status_var.set("Error")

#             if not door_status_response.isError():
#                 door_open = door_status_response.bits[0]
#                 door = "Open" if door_open else "Closed"
#                 door_status_var.set(door)
#             else:
#                 door_status_var.set("Error")

#             if not overheat_alarm_response.isError():
#                 overheat_alarm = overheat_alarm_response.bits[0]
#                 if overheat_alarm:
#                     overheat_alarm_var.set("Overheat Alarm Activated!")
#                 else:
#                     overheat_alarm_var.set("")
#             else:
#                 overheat_alarm_var.set("Error")

#             time.sleep(1)
#         except Exception as e:
#             print(f"Error in update_values: {e}")
#             time.sleep(1)

# # Function to handle window closing
# def on_closing():
#     client.close()
#     root.destroy()

# # Set protocol for window closing
# root.protocol("WM_DELETE_WINDOW", on_closing)

# # Create GUI components
# # Temperature Display
# temp_frame = ttk.Frame(root)
# temp_frame.pack(pady=10)
# ttk.Label(temp_frame, text="Current Temperature:", font=("Arial", 16)).pack(side=tk.LEFT)
# ttk.Label(temp_frame, textvariable=current_temp_var, font=("Arial", 16)).pack(side=tk.LEFT)

# # Humidity Display
# humidity_frame = ttk.Frame(root)
# humidity_frame.pack(pady=10)
# ttk.Label(humidity_frame, text="Current Humidity:", font=("Arial", 16)).pack(side=tk.LEFT)
# ttk.Label(humidity_frame, textvariable=current_humidity_var, font=("Arial", 16)).pack(side=tk.LEFT)

# # Setpoint Adjustment
# setpoint_frame = ttk.Frame(root)
# setpoint_frame.pack(pady=10)
# ttk.Label(setpoint_frame, text="Set Temperature Setpoint:", font=("Arial", 14)).pack()
# setpoint_slider = ttk.Scale(setpoint_frame, from_=0, to=100, orient='horizontal', variable=setpoint_var, command=update_setpoint)
# setpoint_slider.pack()

# # Control Buttons
# button_frame = ttk.Frame(root)
# button_frame.pack(pady=20)
# start_button = ttk.Button(button_frame, text="Start", command=lambda: send_start_stop_command(True))
# start_button.grid(row=0, column=0, padx=10)
# stop_button = ttk.Button(button_frame, text="Stop", command=lambda: send_start_stop_command(False))
# stop_button.grid(row=0, column=1, padx=10)
# emergency_button = ttk.Button(button_frame, text="Emergency Stop", command=send_emergency_stop)
# emergency_button.grid(row=0, column=2, padx=10)

# # Status Indicators
# status_frame = ttk.Frame(root)
# status_frame.pack(pady=10)
# ttk.Label(status_frame, text="System Status:", font=("Arial", 14)).grid(row=0, column=0, sticky=tk.W)
# ttk.Label(status_frame, textvariable=system_status_var, font=("Arial", 14)).grid(row=0, column=1, sticky=tk.W)
# ttk.Label(status_frame, text="Door Status:", font=("Arial", 14)).grid(row=1, column=0, sticky=tk.W)
# ttk.Label(status_frame, textvariable=door_status_var, font=("Arial", 14)).grid(row=1, column=1, sticky=tk.W)
# ttk.Label(status_frame, textvariable=overheat_alarm_var, font=("Arial", 14), foreground="red").grid(row=2, column=0, columnspan=2)

# # Start the background thread to update values
# update_thread = threading.Thread(target=update_values, daemon=True)
# update_thread.start()

# # Start the GUI event loop
# root.mainloop()



# hmi_app.py

import tkinter as tk
from tkinter import ttk, messagebox
from pymodbus.client import ModbusTcpClient
import threading
import time

# PLC Configuration
PLC_IP = 'localhost'  # Connect to the local Modbus server
PLC_PORT = 5020       # Port number matching the server script

# Connect to the PLC
client = ModbusTcpClient(PLC_IP, port=PLC_PORT)

# Check connection
if not client.connect():
    messagebox.showerror("Connection Error", "Unable to connect to PLC.")
    exit()

# Create the main application window
root = tk.Tk()
root.title("Temperature Control System HMI")
root.geometry("800x600")

# Variables for holding values
setpoint_var = tk.DoubleVar()
current_temp_var = tk.StringVar(value="--")
current_humidity_var = tk.StringVar(value="--")
system_status_var = tk.StringVar(value="Stopped")
door_status_var = tk.StringVar(value="Closed")
overheat_alarm_var = tk.StringVar(value="")

# Function to send start/stop command to the PLC
def send_start_stop_command(start):
    client.write_coil(0, start)  # Coil 0: Start_Stop_Button
    if start:
        client.write_coil(1, True)  # Coil 1: Safety_Switch (ensure it's True when starting)
    # System_Enable is updated by PLC logic; we'll read it in update_values()

# Function to send emergency stop command
def send_emergency_stop():
    client.write_coil(1, False)  # Coil 1: Safety_Switch (set to False to stop)
    messagebox.showwarning("Emergency Stop", "Emergency Stop Activated!")

# Function to update setpoint temperature
def update_setpoint(value):
    client.write_register(0, int(float(value)))  # Register 0: Temp_Setpoint

# Function to update displayed values
def update_values():
    while True:
        try:
            # Read current temperature and humidity from PLC
            temp_response = client.read_holding_registers(1, 1)  # Register 1: Temp_Sensor
            humidity_response = client.read_holding_registers(2, 1)  # Register 2: Humidity_Sensor

            if not temp_response.isError():
                current_temp = temp_response.registers[0]
                current_temp_var.set(f"{current_temp} °C")
            else:
                current_temp_var.set("Error")

            if not humidity_response.isError():
                current_humidity = humidity_response.registers[0]
                current_humidity_var.set(f"{current_humidity} %")
            else:
                current_humidity_var.set("Error")

            # Read system status and indicators
            system_enable_response = client.read_coils(2, 1)  # Coil 2: System_Enable
            door_status_response = client.read_discrete_inputs(0, 1)  # Input 0: Door_Sensor
            overheat_alarm_response = client.read_discrete_inputs(1, 1)  # Input 1: Overheat_Alarm

            if not system_enable_response.isError():
                system_enable = system_enable_response.bits[0]
                status = "Running" if system_enable else "Stopped"
                system_status_var.set(status)
            else:
                system_status_var.set("Error")

            if not door_status_response.isError():
                door_open = door_status_response.bits[0]
                door = "Open" if door_open else "Closed"
                door_status_var.set(door)
            else:
                door_status_var.set("Error")

            if not overheat_alarm_response.isError():
                overheat_alarm = overheat_alarm_response.bits[0]
                if overheat_alarm:
                    overheat_alarm_var.set("Overheat Alarm Activated!")
                else:
                    overheat_alarm_var.set("")
            else:
                overheat_alarm_var.set("Error")

            time.sleep(1)
        except Exception as e:
            print(f"Error in update_values: {e}")
            time.sleep(1)

# Function to handle window closing
def on_closing():
    client.close()
    root.destroy()

# Set protocol for window closing
root.protocol("WM_DELETE_WINDOW", on_closing)

# Create GUI components
# Temperature Display
temp_frame = ttk.Frame(root)
temp_frame.pack(pady=10)
ttk.Label(temp_frame, text="Current Temperature:", font=("Arial", 16)).pack(side=tk.LEFT)
ttk.Label(temp_frame, textvariable=current_temp_var, font=("Arial", 16)).pack(side=tk.LEFT)

# Humidity Display
humidity_frame = ttk.Frame(root)
humidity_frame.pack(pady=10)
ttk.Label(humidity_frame, text="Current Humidity:", font=("Arial", 16)).pack(side=tk.LEFT)
ttk.Label(humidity_frame, textvariable=current_humidity_var, font=("Arial", 16)).pack(side=tk.LEFT)

# Setpoint Adjustment
setpoint_frame = ttk.Frame(root)
setpoint_frame.pack(pady=10)
ttk.Label(setpoint_frame, text="Set Temperature Setpoint:", font=("Arial", 14)).pack()
setpoint_slider = ttk.Scale(setpoint_frame, from_=0, to=100, orient='horizontal', variable=setpoint_var, command=update_setpoint)
setpoint_slider.pack()

# Control Buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=20)
start_button = ttk.Button(button_frame, text="Start", command=lambda: send_start_stop_command(True))
start_button.grid(row=0, column=0, padx=10)
stop_button = ttk.Button(button_frame, text="Stop", command=lambda: send_start_stop_command(False))
stop_button.grid(row=0, column=1, padx=10)
emergency_button = ttk.Button(button_frame, text="Emergency Stop", command=send_emergency_stop)
emergency_button.grid(row=0, column=2, padx=10)

# Status Indicators
status_frame = ttk.Frame(root)
status_frame.pack(pady=10)
ttk.Label(status_frame, text="System Status:", font=("Arial", 14)).grid(row=0, column=0, sticky=tk.W)
ttk.Label(status_frame, textvariable=system_status_var, font=("Arial", 14)).grid(row=0, column=1, sticky=tk.W)
ttk.Label(status_frame, text="Door Status:", font=("Arial", 14)).grid(row=1, column=0, sticky=tk.W)
ttk.Label(status_frame, textvariable=door_status_var, font=("Arial", 14)).grid(row=1, column=1, sticky=tk.W)
ttk.Label(status_frame, textvariable=overheat_alarm_var, font=("Arial", 14), foreground="red").grid(row=2, column=0, columnspan=2)

# Start the background thread to update values
update_thread = threading.Thread(target=update_values, daemon=True)
update_thread.start()

# Start the GUI event loop
root.mainloop()