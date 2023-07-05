import socket
import time

host = "localhost"
port = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host, port))
s.listen(0)

print("Server is listening on port", port)

while True:
    conn, address = s.accept()

    print("Receive Connection From ", address)

    # time.sleep(10)
    data = conn.recv(1024)
    conn.sendall(b"{'success': true}")

    conn.close()