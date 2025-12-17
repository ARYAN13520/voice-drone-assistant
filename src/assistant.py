import threading
from pymavlink import mavutil
import time
from src.mavlink_connection import master
from src.command_dispatcher import dispatch
from src.telemetry_state import telemetry, telemetry_ready

CONNECTION_STRING = "udp:127.0.0.1:14550"


def telemetry_loop():
    master.wait_heartbeat()
    print("[Telemetry] Connected")

    first_heartbeat = False

    while True:
        msg = master.recv_match(
            type=["HEARTBEAT", "GLOBAL_POSITION_INT", "VFR_HUD"],
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

            telemetry["mode"] = {
                0: "STABILIZE",
                1: "ACRO",
                2: "ALT_HOLD",
                3: "AUTO",
                4: "GUIDED",
                5: "LOITER",
                6: "RTL",
                9: "LAND",
            }.get(msg.custom_mode, "UNKNOWN")

            # Mark telemetry as ready on first valid heartbeat
            if not first_heartbeat:
                telemetry_ready.set()
                first_heartbeat = True

        elif msg_type == "GLOBAL_POSITION_INT":
            telemetry["altitude"] = msg.relative_alt / 1000.0

        elif msg_type == "VFR_HUD":
            telemetry["groundspeed"] = msg.groundspeed


def assistant_loop():
    print("\nVoice Drone Assistant (Text Mode)")
    print("Type commands in plain English.")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            command = input("Assistant> ").strip()

            if command.lower() == "exit":
                print("Shutting down assistant.")
                break

            if not command:
                continue

            dispatch(command)

        except KeyboardInterrupt:
            print("\nShutting down assistant.")
            break


if __name__ == "__main__":
    telemetry_thread = threading.Thread(
        target=telemetry_loop,
        daemon=True
    )
    telemetry_thread.start()

    print("Waiting for telemetry synchronization...")
    telemetry_ready.wait()
    print("Telemetry synchronized. Assistant ready.")

    assistant_loop()
