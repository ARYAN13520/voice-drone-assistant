from src.safety_gate import check_safety
from src.set_guided_mode import COPTER_MODES
from pymavlink import mavutil
import time

CONNECTION_STRING = 'udp:127.0.0.1:14550'


def set_mode(mode_name: str):
    if not check_safety():
        print("❌ Command blocked by safety gate")
        return

    if mode_name not in COPTER_MODES:
        print(f"❌ Unknown mode: {mode_name}")
        return

    print(f"Setting mode to {mode_name}...")

    master = mavutil.mavlink_connection(CONNECTION_STRING)
    master.wait_heartbeat()

    master.set_mode(COPTER_MODES[mode_name])
    time.sleep(1)

    heartbeat = master.recv_match(type='HEARTBEAT', blocking=True)
    print(f"Mode now: {heartbeat.custom_mode}")


def dispatch(command: str):
    command = command.lower().strip()

    if command == "set mode guided":
        set_mode("GUIDED")
    else:
        print(f"❌ Unknown command: {command}")


if __name__ == "__main__":
    print("Command Dispatcher Ready")
    while True:
        cmd = input(">> ")
        if cmd in ("exit", "quit"):
            break
        dispatch(cmd)
