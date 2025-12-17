from pymavlink import mavutil

CONNECTION_STRING = "udp:127.0.0.1:14550"

print("[MAVLink] Connecting...")
master = mavutil.mavlink_connection(CONNECTION_STRING)
master.wait_heartbeat()
print("[MAVLink] Heartbeat received")
