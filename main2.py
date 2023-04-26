import socket

import threading

import rsa
choice = input("Do you want to host (1) or to connect (2): ")

if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("10.0.0.136", 9999))
    server.listen()

    client, _ = server.accept()

elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("10.0.0.136", 9999))

else:
    exit()


def send_message(client_user):
    while True:
        message = input("")
        client_user.send(message.encode())
        print("You: " + message)


def receive_message(client_user):
    while True:
        print("Other: " + client_user.recv(1024).decode())


threading.Thread(target=send_message, args=(client,)).start()
threading.Thread(target=receive_message, args=(client,)).start()