from pymavlink import mavutil

# CHANGE THIS PORT BASED ON YOUR SETUP
# Examples:
# USB (Pixhawk): '/dev/ttyACM0'
# Telemetry radio: '/dev/ttyUSB0'
# Simulator (UDP): 'udp:127.0.0.1:14550'

CONNECTION_STRING = 'udp:127.0.0.1:14550'
BAUD_RATE = 115200

print("Connecting to vehicle...")
master = mavutil.mavlink_connection(CONNECTION_STRING, baud=BAUD_RATE)

print("Waiting for heartbeat...")
heartbeat = master.recv_match(type='HEARTBEAT', blocking=True)

print("Heartbeat received!")
print(f"System ID: {master.target_system}")
print(f"Component ID: {master.target_component}")
print(f"Autopilot: {heartbeat.autopilot}")
print(f"Vehicle type: {heartbeat.type}")
print(f"Base mode: {heartbeat.base_mode}")
print(f"Custom mode: {heartbeat.custom_mode}")

