from pymavlink import mavutil
from src.safety_gate import check_safety
from src.telemetry_state import telemetry
from src.mavlink_connection import master
import time

CONNECTION_STRING = "udp:127.0.0.1:14550"



def wait_for_telemetry_update(seconds=2):
    start = time.time()
    while time.time() - start < seconds:
        if telemetry["mode"] != "UNKNOWN":
            return
        time.sleep(0.1)

def send_body_velocity(master, vx, vy, vz, yaw_rate=0):
    master.mav.set_position_target_local_ned_send(
        0,
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_FRAME_BODY_NED,
        0b0000111111000111,
        0, 0, 0,
        vx, vy, vz,
        0, 0, 0,
        yaw_rate, 0
    )


# ---------------- MOVEMENT ----------------

def move_forward():
    if not check_safety("move forward", telemetry):
        print("❌ Move blocked")
        return
    print("Moving forward")
    send_body_velocity(master, 1.0, 0, 0)
    time.sleep(1)
    send_body_velocity(master, 0, 0, 0)


def move_back():
    if not check_safety("move back", telemetry):
        print("❌ Move blocked")
        return
    print("Moving backward")
    send_body_velocity(master, -1.0, 0, 0)
    time.sleep(1)
    send_body_velocity(master, 0, 0, 0)


def move_left():
    if not check_safety("move left", telemetry):
        print("❌ Move blocked")
        return
    print("Moving left")
    send_body_velocity(master, 0, -1.0, 0)
    time.sleep(1)
    send_body_velocity(master, 0, 0, 0)


def move_right():
    if not check_safety("move right", telemetry):
        print("❌ Move blocked")
        return
    print("Moving right")
    send_body_velocity(master, 0, 1.0, 0)
    time.sleep(1)
    send_body_velocity(master, 0, 0, 0)


def rotate_left():
    if not check_safety("rotate left", telemetry):
        print("❌ Rotate blocked")
        return
    print("Rotating left")
    send_body_velocity(master, 0, 0, 0, yaw_rate=-0.5)
    time.sleep(1)
    send_body_velocity(master, 0, 0, 0)


def rotate_right():
    if not check_safety("rotate right", telemetry):
        print("❌ Rotate blocked")
        return
    print("Rotating right")
    send_body_velocity(master, 0, 0, 0, yaw_rate=0.5)
    time.sleep(1)
    send_body_velocity(master, 0, 0, 0)


# ---------------- BASIC CONTROL ----------------

def set_mode(mode):
    command = f"set mode {mode.lower()}"
    if not check_safety(command, telemetry):
        print("❌ Command blocked by safety gate")
        return

   
    mode_mapping = master.mode_mapping()

    if mode.upper() not in mode_mapping:
        print(f"Unknown mode: {mode}")
        return

    print(f"Setting mode to {mode}...")
    master.set_mode(mode_mapping[mode.upper()])
    wait_for_telemetry_update()
    print(f"Mode now: {mode}")


def arm():
    if not check_safety("arm", telemetry):
        print("❌ Arm blocked")
        return
    print("Arming vehicle...")
    master.arducopter_arm()
    master.motors_armed_wait()
    print("Vehicle armed")


def takeoff(target_alt=15.0):
    telemetry["last_takeoff_time"] = time.time()
    telemetry["armed"] = True
    if not check_safety("takeoff", telemetry):
        print("❌ Takeoff blocked")
        return

   
    print("Arming...")
    master.arducopter_arm()
    master.motors_armed_wait()
    
    #  FORCE TELEMETRY SYNC
    telemetry["armed"] = True

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


def land():
    if not check_safety("land", telemetry):
        print("❌ Land blocked")
        return
    
    print("Landing...")
    master.set_mode(master.mode_mapping()["LAND"])

def set_rtl():
    if not check_safety("rtl", telemetry):
        print("❌ RTL blocked")
        return

    master = connect()
    print("Switching to RTL...")
    master.set_mode(master.mode_mapping()["RTL"])
    print("Mode now: RTL")


def set_loiter():
    if not check_safety("loiter", telemetry):
        print("❌ Loiter blocked")
        return

    master = connect()
    print("Switching to LOITER...")
    master.set_mode(master.mode_mapping()["LOITER"])
    print("Mode now: LOITER")



# ---------------- DISPATCHER ----------------

def dispatch(command: str):
    command = command.lower().strip()

    # MODE
    if "set mode guided" in command or command == "guided":
        set_mode("GUIDED")
    
    elif "rtl" in command or "return home" in command:
        set_rtl()

    elif "loiter" in command:
        set_loiter()


    # TAKEOFF / LAND
    elif "takeoff" in command:
        takeoff()

    elif "land" in command:
        land()

    elif command == "arm":
        arm()

    # MOVEMENT
    elif "rotate left" in command:
        rotate_left()

    elif "rotate right" in command:
        rotate_right()

    elif "forward" in command:
        move_forward()

    elif "back" in command:
        move_back()

    elif "left" in command:
        move_left()

    elif "right" in command:
        move_right()

    # TELEMETRY QUERIES
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
