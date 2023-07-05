import socket
import time
import json
import uuid

def create(db, db_name):
    db[db_name] = {}

def insert_to(db, db_name, data):
    key = uuid.uuid4().hex
    db[db_name][key] = data
    return key

def delete_from(db, db_name, key):
    del db[db_name][key]

def get_from(db, db_name, key):
    return db[db_name][key]

def list_from(db, db_name):
    return db[db_name]

def convert_to_bytes(json_data):
    return json.dumps(json_data).encode()

def command_handler(db, command, conn):
    print(f"{command} received")
    if command.startswith("createdb"):
        _, db_name=command.split("::")
        create(db, db_name)
        conn.send(convert_to_bytes({'success': True}))
        
    elif command.startswith("insert"):
        _, db_name, data=command.split("::")
        data = json.loads(data)
        key = insert_to(db, db_name, data)
        conn.send(convert_to_bytes({'key': key}))

    elif command.startswith("delete"):
        _, db_name, key=command.split("::")
        delete_from(db, db_name, key)
        conn.send(convert_to_bytes({'key': key}))

    elif command.startswith("get"):
        _, db_name, key=command.split("::")
        data = get_from(db, db_name, key)
        conn.send(convert_to_bytes(data))

    elif command.startswith("list"):
        _, db_name=command.split("::")
        data = list_from(db, db_name)
        conn.send(convert_to_bytes(data))

host = "localhost"
port = 4444

sample_db = {
    "test_db": {
        "12345": { "d": "o", "b": "0"},
        "12346": { "d": "o", "b": "0"}
    }
}

def get_db(db_file_path):
    try:
        with open(db_file_path, "r") as db_file:
            db = json.load(db_file)
    except:
        db = sample_db
    return db

def persist_db(db, db_file_path):
    with open(db_file_path, "w") as db_file:
        json.dump(db, db_file, indent=2)

def initial_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Avoid bind() exception: OSError: [Errno 48] Address already in use
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((host, port))
    s.listen(0)

    return s

def main():
    print("In-mem Document DB is listening on port", port) 
    with initial_socket(host, port) as s:
        while True:
            try:
                db = get_db("./db.json")
                conn, address = s.accept()
                with conn:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        commands = data.decode()
                        for command in commands.split(";"):
                            command_handler(db, command, conn)
                persist_db(db, "./db.json")
            except Exception as ex:
                print(f"Error: {ex}")

# def main():
#     with s:
#         while True:
#             conn, address = s.accept()
#             with conn:
#                 # TODO: Don't know why this code is not working, loop forever
#                 commands = ""
#                 while True:
#                     data = conn.recv(1024)
#                     if not data:
#                         break
#                     commands += data.decode()

#                 for command in commands.split(";"):
#                     command_handler(command, conn)
  
main()