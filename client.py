import socket
import time

host = "localhost"
port = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((host, port))

print("Connecting to", host, "on port", port)

s.send(b"Hello, server")

resp = s.recv(1024)

print("Response from server:", resp.decode("utf-8"))