import socket
from threading import Thread

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = dict()


def broadcast(message):
    for client in clients.values():
        client.send(message)

def handle_connection(client):
    stop = False
    while not stop:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            nickname = list(clients.keys())[list(client.values()).index(client)]
            clients.pop(nickname)
            broadcast(f'Client {nickname} left the chat'.encode('utf-8'))
            stop = True


def main():
    print("Server is running...")
    while True:
        client, address = server.accept()
        print(f"Connected to {address}")

        client.send("NICK".encode("utf-8"))

        nickname = client.recv(1024).decode("utf-8")
        clients[nickname] = client
        print(f"Nickname is {nickname}")

        broadcast(f"{nickname} joined the chat!".encode("utf-8"))

        client.send("You are connected!".encode("utf-8"))

        thread = Thread(target=handle_connection, args=(client,))
        thread.start()


if __name__=="__main__":
    main()
