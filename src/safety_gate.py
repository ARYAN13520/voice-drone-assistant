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

def check_safety(command, telemetry):
    # Allow mode change commands unconditionally (safe)
    if "mode" in command:
        return True

    # For all other commands, enforce safety
    if telemetry["mode"] != "GUIDED":
        print("❌ SAFETY BLOCK: Vehicle not in GUIDED mode")
        return False

    if telemetry["armed"]:
        print("❌ SAFETY BLOCK: Vehicle is armed")
        return False

    return True


if __name__ == "__main__":
    allowed = check_safety()
    print(f"Command allowed: {allowed}")

