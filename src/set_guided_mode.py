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

def set_guided_mode():
    print("Running safety gate...")
    if check_safety():
        print("Already safe or ready. Exiting.")
        return

    print("Connecting to vehicle...")
    master = mavutil.mavlink_connection(CONNECTION_STRING)

    print("Waiting for heartbeat...")
    master.wait_heartbeat()

    print("Requesting GUIDED mode...")
    master.set_mode(COPTER_MODES["GUIDED"])

    time.sleep(1)

    heartbeat = master.recv_match(type='HEARTBEAT', blocking=True)
    print(f"New mode ID: {heartbeat.custom_mode}")


if __name__ == "__main__":
    set_guided_mode()

