import socket
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 6380))

while True:
    sys.stdout.write("> ")
    sys.stdout.flush()

    line = sys.stdin.buffer.readline()
    if not line:
        break

    try:
        command = line.decode('utf-8').strip()
    except UnicodeDecodeError:
        print("Ошибка кодировки — введи ещё раз")
        continue

    if not command:
        break

    client.send(f"{command}\n".encode())
    response = client.recv(1024)
    print(response.decode().strip())

client.close()