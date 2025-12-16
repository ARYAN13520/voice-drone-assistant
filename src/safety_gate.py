from pymavlink import mavutil

CONNECTION_STRING = 'udp:127.0.0.1:14550'

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

def check_safety():
    print("Connecting to vehicle...")
    master = mavutil.mavlink_connection(CONNECTION_STRING)

    print("Waiting for heartbeat...")
    heartbeat = master.recv_match(type='HEARTBEAT', blocking=True)

    mode_id = heartbeat.custom_mode
    mode = COPTER_MODES.get(mode_id, "UNKNOWN")

    armed = bool(
        heartbeat.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
    )

    print(f"Mode detected: {mode}")
    print(f"Armed state: {'ARMED' if armed else 'DISARMED'}")

    if mode != "GUIDED":
        print("❌ SAFETY BLOCK: Vehicle not in GUIDED mode")
        return False

    print("✅ SAFETY PASS: Command execution allowed")
    return True


if __name__ == "__main__":
    allowed = check_safety()
    print(f"Command allowed: {allowed}")

