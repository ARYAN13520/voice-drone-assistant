from pymavlink import mavutil

CONNECTION_STRING = 'udp:127.0.0.1:14550'

print("Connecting to vehicle...")
master = mavutil.mavlink_connection(CONNECTION_STRING)

print("Waiting for heartbeat...")
heartbeat = master.recv_match(type='HEARTBEAT', blocking=True)

armed = bool(
    heartbeat.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
)

print("Heartbeat received!")
print(f"Armed state: {'ARMED' if armed else 'DISARMED'}")

