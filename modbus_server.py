# # # modbus_server.py

# # from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
# # from pymodbus.datastore import ModbusSequentialDataBlock
# # #from pymodbus.server.sync import StartTcpServer
# # from pymodbus.device import ModbusDeviceIdentification


# # from pymodbus.server import StartTcpServer  # Updated import
# # from pymodbus.device import ModbusDeviceIdentification
# # from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
# # from pymodbus.datastore import ModbusSequentialDataBlock
# # import threading
# # import time

# # def run_server():
# #     # Initialize data store with default values
# #     store = ModbusSlaveContext(
# #         di=ModbusSequentialDataBlock(0, [0]*100),  # Discrete Inputs (read-only bits)
# #         co=ModbusSequentialDataBlock(0, [0]*100),  # Coils (read/write bits)
# #         hr=ModbusSequentialDataBlock(0, [0]*100),  # Holding Registers (read/write words)
# #         ir=ModbusSequentialDataBlock(0, [0]*100)   # Input Registers (read-only words)
# #     )
# #     context = ModbusServerContext(slaves=store, single=True)

# #     # Server identity
# #     identity = ModbusDeviceIdentification()
# #     identity.VendorName = 'Python Modbus Simulator'
# #     identity.ProductCode = 'PMS'
# #     identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
# #     identity.ProductName = 'Python Modbus Server'
# #     identity.ModelName = 'Pymodbus'
# #     identity.MajorMinorRevision = '1.5'

# #     # Start the server in a new thread
# #     server_thread = threading.Thread(target=StartTcpServer, args=(context,), kwargs={
# #         'identity': identity,
# #         'address': ("localhost", 5020)
# #     })
# #     server_thread.daemon = True
# #     server_thread.start()
# #     print("Modbus server is running on localhost:5020")

# #     # Simulate PLC behavior
# #     simulate_plc_behavior(context)

# # def simulate_plc_behavior(context):
# #     while True:
# #         # Access the data store
# #         slave_id = 0x00  # Slave ID 0
# #         store = context[slave_id]

# #         # Read current values
# #         coils = store.getValues(1, 0, count=10)  # Function code 1: Coils
# #         discretes = store.getValues(2, 0, count=10)  # Function code 2: Discrete Inputs
# #         holding_registers = store.getValues(3, 0, count=10)  # Function code 3: Holding Registers
# #         input_registers = store.getValues(4, 0, count=10)  # Function code 4: Input Registers

# #         # Simulate temperature sensor (Register 1: Temp_Sensor)
# #         temp_sensor = holding_registers[1]
# #         temp_setpoint = holding_registers[0]
# #         system_enable = coils[2]  # Coil 2: System_Enable

# #         if system_enable:
# #             # Adjust temperature towards setpoint
# #             if temp_sensor < temp_setpoint:
# #                 temp_sensor += 1
# #             elif temp_sensor > temp_setpoint:
# #                 temp_sensor -= 1
# #         else:
# #             # Cool down to ambient temperature (e.g., 20°C)
# #             if temp_sensor > 20:
# #                 temp_sensor -= 1
# #             elif temp_sensor < 20:
# #                 temp_sensor += 1

# #         # Update Overheat Alarm (Discrete Input 1)
# #         if temp_sensor > 80:
# #             discretes[1] = 1  # Overheat Alarm activated
# #         else:
# #             discretes[1] = 0  # Overheat Alarm deactivated

# #         # Simulate humidity sensor (Register 2: Humidity_Sensor)
# #         humidity_sensor = 50 + 10 * (time.time() % 10) / 10  # Varies between 50% and 60%

# #         # Update the data store
# #         holding_registers[1] = int(temp_sensor)
# #         holding_registers[2] = int(humidity_sensor)
# #         store.setValues(3, 1, [holding_registers[1]])  # Update Temp_Sensor
# #         store.setValues(3, 2, [holding_registers[2]])  # Update Humidity_Sensor
# #         store.setValues(2, 1, [discretes[1]])  # Update Overheat Alarm

# #         # Simulate Door Sensor (Discrete Input 0)
# #         # For simplicity, keep it closed (0)
# #         store.setValues(2, 0, [0])

# #         time.sleep(1)

# # if __name__ == "__main__":
# #     run_server()


# # modbus_server.py

# from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
# from pymodbus.datastore import ModbusSequentialDataBlock
# from pymodbus.server import StartTcpServer
# from pymodbus.device import ModbusDeviceIdentification
# import threading
# import time

# def simulate_plc_behavior(context):
#     while True:
#         # Access the data store
#         slave_id = 0x00  # Slave ID 0
#         store = context[slave_id]

#         # Read current values
#         coils = store.getValues(1, 0, count=10)  # Function code 1: Coils
#         discretes = store.getValues(2, 0, count=10)  # Function code 2: Discrete Inputs
#         holding_registers = store.getValues(3, 0, count=10)  # Function code 3: Holding Registers

#         # Simulate temperature sensor (Register 1: Temp_Sensor)
#         temp_sensor = holding_registers[1]
#         temp_setpoint = holding_registers[0]
#         system_enable = coils[2]  # Coil 2: System_Enable

#         if system_enable:
#             # Adjust temperature towards setpoint
#             if temp_sensor < temp_setpoint:
#                 temp_sensor += 1
#             elif temp_sensor > temp_setpoint:
#                 temp_sensor -= 1
#         else:
#             # Cool down to ambient temperature (e.g., 20°C)
#             if temp_sensor > 20:
#                 temp_sensor -= 1
#             elif temp_sensor < 20:
#                 temp_sensor += 1

#         # Update Overheat Alarm (Discrete Input 1)
#         if temp_sensor > 80:
#             discretes[1] = 1  # Overheat Alarm activated
#         else:
#             discretes[1] = 0  # Overheat Alarm deactivated

#         # Simulate humidity sensor (Register 2: Humidity_Sensor)
#         humidity_sensor = 50 + 10 * (time.time() % 10) / 10  # Varies between 50% and 60%

#         # Update the data store
#         holding_registers[1] = int(temp_sensor)
#         holding_registers[2] = int(humidity_sensor)
#         store.setValues(3, 1, [holding_registers[1]])  # Update Temp_Sensor
#         store.setValues(3, 2, [holding_registers[2]])  # Update Humidity_Sensor
#         store.setValues(2, 1, [discretes[1]])  # Update Overheat Alarm

#         # Simulate Door Sensor (Discrete Input 0)
#         # For simplicity, keep it closed (0)
#         store.setValues(2, 0, [0])

#         time.sleep(1)

# def run_server():
#     # Initialize data store with default values
#     store = ModbusSlaveContext(
#         di=ModbusSequentialDataBlock(0, [0]*100),  # Discrete Inputs
#         co=ModbusSequentialDataBlock(0, [0]*100),  # Coils
#         hr=ModbusSequentialDataBlock(0, [0]*100),  # Holding Registers
#         ir=ModbusSequentialDataBlock(0, [0]*100)   # Input Registers
#     )
#     context = ModbusServerContext(slaves=store, single=True)

#     # Server identity
#     identity = ModbusDeviceIdentification()
#     identity.VendorName = 'Python Modbus Simulator'
#     identity.ProductCode = 'PMS'
#     identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
#     identity.ProductName = 'Python Modbus Server'
#     identity.ModelName = 'Pymodbus'
#     identity.MajorMinorRevision = '1.5'

#     # Start the simulate_plc_behavior in a new thread
#     plc_thread = threading.Thread(target=simulate_plc_behavior, args=(context,))
#     plc_thread.daemon = True
#     plc_thread.start()

#     # Start the server
#     print("Modbus server is running on localhost:5020")
#     StartTcpServer(context=context, identity=identity, address=("localhost", 5020))

# if __name__ == "__main__":
#     run_server()


# modbus_server.py

from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
import threading
import time

def simulate_plc_behavior(context):
    while True:
        # Access the data store
        slave_id = 0x00  # Slave ID 0
        store = context[slave_id]

        # Read current values
        coils = store.getValues(1, 0, count=10)        # Function code 1: Coils
        discretes = store.getValues(2, 0, count=10)    # Function code 2: Discrete Inputs
        holding_registers = store.getValues(3, 0, count=10)  # Function code 3: Holding Registers

        # Read inputs
        start_stop_button = coils[0]  # Coil 0: Start_Stop_Button
        safety_switch = coils[1]      # Coil 1: Safety_Switch
        door_sensor = discretes[0]    # Discrete Input 0: Door_Sensor

        # Determine System_Enable (Coil 2)
        system_enable = start_stop_button and safety_switch and not door_sensor
        coils[2] = system_enable  # Update Coil 2: System_Enable

        # Update coils in the store
        store.setValues(1, 0, coils)

        # Simulate temperature sensor (Register 1: Temp_Sensor)
        temp_sensor = holding_registers[1]
        temp_setpoint = holding_registers[0]

        if system_enable:
            # Adjust temperature towards setpoint
            if temp_sensor < temp_setpoint:
                temp_sensor += 1
            elif temp_sensor > temp_setpoint:
                temp_sensor -= 1
        else:
            # Cool down to ambient temperature (e.g., 20°C)
            if temp_sensor > 20:
                temp_sensor -= 1
            elif temp_sensor < 20:
                temp_sensor += 1

        # Update Overheat Alarm (Discrete Input 1)
        if temp_sensor > 80:
            discretes[1] = 1  # Overheat Alarm activated
        else:
            discretes[1] = 0  # Overheat Alarm deactivated

        # Simulate humidity sensor (Register 2: Humidity_Sensor)
        humidity_sensor = 50 + 10 * (time.time() % 10) / 10  # Varies between 50% and 60%

        # Update the data store
        holding_registers[1] = int(temp_sensor)
        holding_registers[2] = int(humidity_sensor)
        store.setValues(3, 1, [holding_registers[1]])  # Update Temp_Sensor
        store.setValues(3, 2, [holding_registers[2]])  # Update Humidity_Sensor
        store.setValues(2, 1, [discretes[1]])          # Update Overheat Alarm

        # Simulate Door Sensor (Discrete Input 0)
        # For simplicity, keep it closed (0)
        store.setValues(2, 0, [0])

        time.sleep(1)

def run_server():
    # Initialize data store with default values
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*100),  # Discrete Inputs
        co=ModbusSequentialDataBlock(0, [0]*100),  # Coils
        hr=ModbusSequentialDataBlock(0, [20]*100),  # Holding Registers (Initialize Temp_Sensor to 20)
        ir=ModbusSequentialDataBlock(0, [0]*100)   # Input Registers
    )
    context = ModbusServerContext(slaves=store, single=True)

    # Server identity
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Python Modbus Simulator'
    identity.ProductCode = 'PMS'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Python Modbus Server'
    identity.ModelName = 'Pymodbus'
    identity.MajorMinorRevision = '1.5'

    # Start the simulate_plc_behavior in a new thread
    plc_thread = threading.Thread(target=simulate_plc_behavior, args=(context,))
    plc_thread.daemon = True
    plc_thread.start()

    # Start the server
    print("Modbus server is running on localhost:5020")
    StartTcpServer(context=context, identity=identity, address=("localhost", 5020))

if __name__ == "__main__":
    run_server()