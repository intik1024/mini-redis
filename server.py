import socket
from store import Store

store=Store()

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('localhost',6380))
server.listen()
print("Сервер слушает по порту 6380")

while True:
    conn, addr = server.accept()
    print(f'Подключился: {addr}')
    while True:
        data=conn.recv(1024)

        if not data:
            break

        try:
            command = data.decode().strip()
        except UnicodeDecodeError:
            conn.send(b"ERROR: bad encoding\n")
            continue

        parts=command.split(maxsplit=2)

        if not parts:
            continue

        if parts[0]=='PING':
            conn.send(b"PONG\n")
        elif parts[0]=='SET':
            if len(parts)<3:
                conn.send(b'ERROR\n')
                continue
            key=parts[1]
            value=parts[2]
            store.set(key,value)
            conn.send(b'OK\n')

        elif parts[0]=='GET':
            if len(parts)<2:
                conn.send(b'ERROR\n')
                continue
            key=parts[1]
            value=store.get(key)
            if value is None:
                conn.send(b'(nil)\n')
            else:
                conn.send(f'{value}\n'.encode())

        elif parts[0]=='DEL':
            if len(parts) < 2:
                conn.send(b'ERROR\n')
                continue
            key=parts[1]
            store.delete(key)
            conn.send(b'OK\n')
        elif parts[0]=='EXPIRE':
            if len(parts)<3:
                conn.send(b'ERROR\n')
                continue
            key=parts[1]
            try:
                seconds = int(parts[2])
            except ValueError:
                conn.send(b'ERROR\n')
                continue

            if store.expire(key,seconds):
                conn.send(b'OK\n')
            else:
                conn.send(b'(nil)\n')
        else:
            conn.send(b"UNKNOWN\n")

    conn.close()
