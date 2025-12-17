import threading
import time
from pymavlink import mavutil

from src.command_dispatcher import dispatch
from src.telemetry_state import telemetry

CONNECTION_STRING = "udp:127.0.0.1:14550"

COPTER_MODES = {
    0: "STABILIZE",
    1: "ACRO",
    2: "ALT_HOLD",
    3: "AUTO",
    4: "GUIDED",
    5: "LOITER",
    6: "RTL",
    9: "LAND",
}

def telemetry_loop():
    master = mavutil.mavlink_connection(CONNECTION_STRING)
    master.wait_heartbeat()
    print("[Telemetry] Connected")

    while True:
        msg = master.recv_match(
            type=["HEARTBEAT", "GLOBAL_POSITION_INT", "VFR_HUD"],
            blocking=True,
            timeout=1
        )

        if not msg:
            continue

        t = msg.get_type()

        if t == "HEARTBEAT":
            telemetry["armed"] = bool(
                msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
            )
            telemetry["mode"] = COPTER_MODES.get(msg.custom_mode, "UNKNOWN")

        elif t == "GLOBAL_POSITION_INT":
            telemetry["altitude"] = msg.relative_alt / 1000.0

        elif t == "VFR_HUD":
            telemetry["groundspeed"] = msg.groundspeed


def assistant_loop():
    print("\nVoice Drone Assistant (Text Mode)")
    print("Type commands in plain English.")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            command = input("Assistant> ").strip().lower()
        except KeyboardInterrupt:
            break

        if command == "exit":
            break

        dispatch(command)

    print("Shutting down assistant.")


if __name__ == "__main__":
    t = threading.Thread(target=telemetry_loop, daemon=True)
    t.start()

    time.sleep(1)  # let telemetry warm up
    assistant_loop()
