from pymavlink import mavutil
import time
from src.safety_gate import check_safety

CONNECTION_STRING = 'udp:127.0.0.1:14550'

COPTER_MODES = {
    "STABILIZE": 0,
    "ACRO": 1,
    "ALT_HOLD": 2,
    "AUTO": 3,
    "GUIDED": 4,
    "LOITER": 5,
    "RTL": 6,
    "LAND": 9,
}

print("Running safety gate...")
if check_safety():
	print("Already safe or ready. Exiting.")
	exit(0)

print("Connecting to vehicle...")
master = mavutil.mavlink_connection(CONNECTION_STRING)

print("Waiting for heartbeat...")
master.wait_heartbeat()

print("Requesting GUIDED mode...")
master.set_mode(COPTER_MODES["GUIDED"])

time.sleep(1)

heartbeat = master.recv_match(type='HEARTBEAT', blocking=True)
print(f"New mode ID: {heartbeat.custom_mode}")

# Read current mode
heartbeat = master.recv_match(type='HEARTBEAT', blocking=True)
current_mode_id = heartbeat.custom_mode
current_mode = [k for k, v in COPTER_MODES.items() if v == current_mode_id]
current_mode = current_mode[0] if current_mode else "UNKNOWN"

print(f"Current mode: {current_mode}")

if current_mode == "GUIDED":
    print("Already in GUIDED mode. No action taken.")
else:
    print("Requesting GUIDED mode...")

    master.set_mode(COPTER_MODES["GUIDED"])

    time.sleep(1)

    heartbeat = master.recv_match(type='HEARTBEAT', blocking=True)
    new_mode_id = heartbeat.custom_mode
    new_mode = [k for k, v in COPTER_MODES.items() if v == new_mode_id]
    new_mode = new_mode[0] if new_mode else "UNKNOWN"

    print(f"New mode: {new_mode}")
