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
    7: "CIRCLE",
    9: "LAND",
    11: "DRIFT",
    13: "SPORT",
    14: "FLIP",
    15: "AUTOTUNE",
    16: "POSHOLD",
    17: "BRAKE",
    18: "THROW",
    19: "AVOID_ADSB",
    20: "GUIDED_NOGPS",
    21: "SMART_RTL",
    22: "FLOWHOLD",
    23: "FOLLOW",
    24: "ZIGZAG",
    25: "SYSTEMID",
    26: "AUTOROTATE",
    27: "AUTO_RTL",
}

print("Connecting to vehicle...")
master = mavutil.mavlink_connection(CONNECTION_STRING)

print("Waiting for heartbeat...")
heartbeat = master.recv_match(type='HEARTBEAT', blocking=True)

mode_id = heartbeat.custom_mode
mode_name = COPTER_MODES.get(mode_id, "UNKNOWN")

print("Heartbeat received!")
print(f"System ID: {master.target_system}")
print(f"Component ID: {master.target_component}")
print(f"Autopilot: {heartbeat.autopilot}")
print(f"Vehicle type: {heartbeat.type}")
print(f"Flight mode: {mode_name} ({mode_id})")
