import time
from pymavlink import mavutil
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

def get_mode(custom_mode):
    return COPTER_MODES.get(custom_mode, "UNKNOWN")

print("Connecting to vehicle...")
master = mavutil.mavlink_connection(CONNECTION_STRING)
master.wait_heartbeat()
print("Telemetry stream started")

try:
    while True:
        msg = master.recv_match(
            type=["GLOBAL_POSITION_INT", "VFR_HUD", "HEARTBEAT"],
            blocking=True,
            timeout=1
        )

        if not msg:
            continue

        msg_type = msg.get_type()

        if msg_type == "HEARTBEAT":
            telemetry["armed"] = bool(
                msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
            )
            telemetry["mode"] = get_mode(msg.custom_mode)

        elif msg_type == "GLOBAL_POSITION_INT":
            telemetry["altitude"] = msg.relative_alt / 1000.0  # meters

        elif msg_type == "VFR_HUD":
            telemetry["groundspeed"] = msg.groundspeed

        print(
            f"MODE: {telemetry['mode']:<8} | "
            f"ARMED: {'YES' if telemetry['armed'] else 'NO ':<3} | "
            f"ALT: {telemetry['altitude']:5.2f} m | "
            f"GS: {telemetry['groundspeed']:4.1f} m/s"
        )

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nTelemetry stopped.")
