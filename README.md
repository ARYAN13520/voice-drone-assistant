# Voice-Controlled Drone Assistant (MAVLink / ArduPilot)
A safety-first, MAVLink-based drone control assistant that enables
natural-language command execution over telemetry using ArduPilot SITL.
This project implements a voice- and text-controlled drone assistant for ArduPilot-based vehicles using MAVLink.
The system provides safety-gated command execution, real-time telemetry synchronization, and modular command routing.
It is designed as a lightweight ground control interface capable of controlling simulated or real UAVs via guided flight commands.

## System Architecture

User Command (Voice / Text)
        ↓
Assistant Interface
        ↓
Command Dispatcher
        ↓
Safety Gate (Telemetry-based validation)
        ↓
MAVLink Command Sender
        ↓
ArduPilot (SITL / Real Vehicle)

Parallel Process:
Telemetry Listener → Shared Telemetry State

## Project Structure

src/
├── assistant.py            # Main assistant loop
├── command_dispatcher.py   # Routes commands to actions
├── safety_gate.py          # Safety validation logic
├── telemetry_state.py      # Shared telemetry state
├── mavlink_connection.py   # MAVLink connection abstraction

## How It Works

- A background telemetry thread continuously updates vehicle state.
- User commands are normalized and dispatched.
- Every command passes through a safety gate that checks mode, arming state, and flight conditions.
- Only validated commands are sent to the vehicle via MAVLink.
- The system prevents unsafe actions such as movement without arming or incorrect flight modes.

## Example Commands

- set mode guided
- takeoff
- land
- go forward
- go left
- rotate right


### Key Design Principles

- **Safety First**  
  All commands are validated against vehicle state (mode, arm status)
  before execution.

- **Single Command Entry Point**  
  All user intents flow through a central dispatcher to avoid
  duplicated logic.

- **Modular & Extensible**  
  Voice input, UI controls, and autonomy can be added without
  changing core control logic.

- **Simulation-Ready**  
  Built and tested using ArduPilot SITL for zero-risk development.

## Features & Capabilities

- MAVLink communication using `pymavlink`
- ArduPilot SITL integration (Copter)
- Real-time heartbeat monitoring
- Flight mode detection and decoding
- Safe switching to `GUIDED` mode
- Arm-state detection (read-only)
- Central safety gate for all commands
- Command dispatcher with intent routing
- Text-based assistant interface with natural-language aliases

### Safety Guarantees

- No command executes unless the vehicle is in `GUIDED` mode
- No implicit arming or takeoff logic
- All control paths pass through a single safety gate
- Designed to mirror real GCS safety behavior




## How to Run (Simulation)

### Prerequisites

- Ubuntu 22.04+ (WSL2 supported)
- Python 3.10+
- ArduPilot SITL
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/ARYAN13520/voice-drone-assistant.git
cd voice-drone-assistant

### 2. Create Virtual Environment

python3 -m venv .voice-venv
source .voice-venv/bin/activate
pip install pymavlink

### 3. Start ArduPilot SITL (Copter)

sim_vehicle.py -v ArduCopter --console --map --out=udp:127.0.0.1:14550

### 4. Run the Assistent

python -m src.assistant

```Example Commands
```guided
```help
```exit



## Safety Notice

This project is intended for simulation and controlled testing environments.
Always validate safety logic thoroughly before deploying on real hardware.

⚠️ Make sure the markdown fences are correct.

Save and exit.

---

## VERIFY

Run:
```bash
sed -n '1,300p' README.md




## Roadmap & Future Work

- [x] MAVLink heartbeat monitoring
- [x] Flight mode decoding
- [x] Safety-gated command execution
- [x] Text-based assistant interface
- [ ] Arm / disarm commands with safety confirmations
- [ ] Guided takeoff and landing
- [ ] Telemetry streaming (altitude, GPS, velocity)
- [ ] Voice input using speech-to-text (Whisper / Vosk)
- [ ] Web-based dashboard (optional)
- [ ] Deployment on Raspberry Pi as companion computer
