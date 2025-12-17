from pymavlink import mavutil
from src.safety_gate import check_safety
from src.telemetry_state import telemetry

CONNECTION_STRING = "udp:127.0.0.1:14550"

def set_mode(mode):
    command = f"set mode {mode.lower()}"

    if not check_safety(command, telemetry):
        print("❌ Command blocked by safety gate")
        return

    print("Connecting to vehicle...")
    master = mavutil.mavlink_connection(CONNECTION_STRING)
    master.wait_heartbeat()

    mode_mapping = master.mode_mapping()
    if mode.upper() not in mode_mapping:
        print(f"Unknown mode: {mode}")
        return

    print(f"Setting mode to {mode}...")
    master.set_mode(mode_mapping[mode.upper()])
    print(f"Mode now: {mode}")

def dispatch(command: str):
    command = command.lower().strip()

    if "guided" in command:
        set_mode("GUIDED")
    else:
        print("Unknown command")
