import socket
import time

host = "localhost"
port = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with s:
    s.connect((host, port))

    print("Connecting to", host, "on port", port)

    # s.send(b"get::test_db::12345")
    # s.send(b"createdb::client-db;")
    s.send(b"insert::client-db::{\"testing1\":\"value\"};")
    # s.send(b"list::client-db")
    
    data = s.recv(1024)
    resp = data.decode()
    
    print("Response from server:", resp)

# with s:
#     s.connect((host, port))
#     s.send(b"createdb::client-db;")
#     s.send(b"insert::client-db::{'testing1':'value'};")
#     s.send(b"insert::client-db::{'testing2':'value2'};")
#     s.send(b"insert::client-db::{'testing2':'value2'};")
#     s.send(b"list::test_db")

#     # TODO: Don't know why this is not working, loop forever
#     resp = ""
#     while True:
#         data = s.recv(1024)
#         if not data:
#             break
#         resp += ";".join(data.decode())

