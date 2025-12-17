from pymavlink import mavutil
import time

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
    command = command.lower()

    mode = telemetry.get("mode", "UNKNOWN")
    armed = telemetry.get("armed", False)
    altitude = telemetry.get("altitude", 0.0)

    # -------------------------------------------------
    # MODE SWITCHING — ALWAYS ALLOWED
    # -------------------------------------------------
    if "mode" in command:
        return True

    # -------------------------------------------------
    # TAKEOFF
    # -------------------------------------------------
    if "takeoff" in command:
        if mode != "GUIDED":
            print("❌ SAFETY BLOCK: Not in GUIDED mode")
            return False

        if altitude > 0.5:
            print("❌ SAFETY BLOCK: Already airborne")
            return False

        return True

    # -------------------------------------------------
    # LAND — ALWAYS ALLOWED
    # -------------------------------------------------
    if "land" in command:
        return True

    # -------------------------------------------------
    # ARM
    # -------------------------------------------------
    if command == "arm":
        if armed:
            print("❌ SAFETY BLOCK: Already armed")
            return False
        return True

    # -------------------------------------------------
    # MOVEMENT (REQUIRES GUIDED + ARMED)
    # -------------------------------------------------
    if any(word in command for word in ["forward", "back", "left", "right", "rotate"]):
        if mode != "GUIDED":
            print("❌ SAFETY BLOCK: Not in GUIDED mode")
            return False

        if not armed:
            print("❌ SAFETY BLOCK: Vehicle not armed")
            return False

        return True

    # -------------------------------------------------
    # DEFAULT
    # -------------------------------------------------
    print("❌ SAFETY BLOCK: Unknown or unsafe command")
    return False


    # -------------------------------------------------
    # RTL / LOITER — ALWAYS ALLOWED
    # -------------------------------------------------
    if "rtl" in command or "loiter" in command:
        return True


if __name__ == "__main__":
    allowed = check_safety()
    print(f"Command allowed: {allowed}")


