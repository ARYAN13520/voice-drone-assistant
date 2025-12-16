from src.command_dispatcher import dispatch

INTRO = """
Voice Drone Assistant (Text Mode)
Type commands in plain English.
Type 'help' to see available commands.
Type 'exit' to quit.
"""

HELP_TEXT = """
Available commands:
- set mode guided
- guided
- go guided
- exit
"""

def normalize_command(user_input: str) -> str:
    text = user_input.lower().strip()

    if text in ("guided", "go guided", "switch to guided"):
        return "set mode guided"

    return text


def assistant_loop():
    print(INTRO)

    while True:
        user_input = input("Assistant> ")

        if user_input.lower() in ("exit", "quit"):
            print("Assistant> Shutting down.")
            break

        if user_input.lower() == "help":
            print(HELP_TEXT)
            continue

        command = normalize_command(user_input)
        dispatch(command)


if __name__ == "__main__":
    assistant_loop()
