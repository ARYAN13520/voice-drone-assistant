import socket
from src.command_dispatcher import dispatch

HOST = "127.0.0.1"
PORT = 5555

print("Starting Assistant Server...")
print(f"Listening on {HOST}:{PORT}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

conn, addr = server.accept()
print(f"Connected by {addr}")

try:
    while True:
        data = conn.recv(1024)
        if not data:
            break

        command = data.decode("utf-8").strip()
        print(f"Received command: {command}")

        dispatch(command)

except KeyboardInterrupt:
    print("Shutting down server.")

finally:
    conn.close()
    server.close()

