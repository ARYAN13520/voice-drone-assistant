from pymavlink import mavutil
from src.safety_gate import check_safety
from src.telemetry_state import telemetry
import time

CONNECTION_STRING = "udp:127.0.0.1:14550"

def connect():
    master = mavutil.mavlink_connection(CONNECTION_STRING)
    master.wait_heartbeat()
    return master

def set_mode(mode):
    command = f"set mode {mode.lower()}"

    if not check_safety(command, telemetry):
        print("❌ Command blocked by safety gate")
        return

    master = connect()
    mode_mapping = master.mode_mapping()

    if mode.upper() not in mode_mapping:
        print(f"Unknown mode: {mode}")
        return

    print(f"Setting mode to {mode}...")
    master.set_mode(mode_mapping[mode.upper()])
    print(f"Mode now: {mode}")

def arm():
    if not check_safety("arm", telemetry):
        print("❌ Arm blocked")
        return

    master = connect()
    print("Arming vehicle...")
    master.arducopter_arm()
    master.motors_armed_wait()
    print("Vehicle armed")

def land():
    if not check_safety("land", telemetry):
        print("❌ Land blocked")
        return

    master = connect()
    print("Landing...")
    master.set_mode(master.mode_mapping()["LAND"])

def takeoff(target_alt=3.0):
    if not check_safety("takeoff", telemetry):
        print("❌ Takeoff blocked")
        return

    master = connect()
    print("Arming...")
    master.arducopter_arm()
    master.motors_armed_wait()

    print(f"Taking off to {target_alt} meters")
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0,
        0, 0, 0, 0,
        0, 0,
        target_alt
    )

def dispatch(command: str):
    command = command.lower().strip()

    # --- MODE CONTROL ---
    if "set mode guided" in command or command == "guided":
        set_mode("GUIDED")

    # --- TAKEOFF / LAND ---
    elif "takeoff" in command:
        takeoff()

    elif "land" in command:
        land()

    elif command == "arm":
        arm()

    # --- TELEMETRY QUERIES (READ-ONLY) ---
    elif "what mode" in command:
        print(f"Current mode is {telemetry['mode']}")

    elif "armed" in command:
        state = "armed" if telemetry["armed"] else "disarmed"
        print(f"Drone is {state}")

    elif "altitude" in command:
        print(f"Altitude is {telemetry['altitude']:.2f} meters")

    elif "speed" in command:
        print(f"Ground speed is {telemetry['groundspeed']:.2f} m/s")

    else:
        print("Unknown command")

