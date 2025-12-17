import threading

telemetry_ready = threading.Event()

telemetry = {
    "mode": "UNKNOWN",
    "armed": False,
    "altitude": 0.0,
    "groundspeed": 0.0
}

