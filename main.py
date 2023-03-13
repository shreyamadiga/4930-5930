import socket
import threading

import rsa

public_key, private_key = rsa.newkeys(1024)
public_other = None

choice = input("Do you want to host (1) or to connect (2): ")

if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("10.0.0.41", 9999))
    server.listen()

    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_other = rsa.PublicKey.load_pkcs1(client.recv(1024))
elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("10.0.0.41", 9999))
    public_other = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))
else:
    exit()


def send_message(client_user):
    while True:
        message = input("")
        client_user.send(rsa.encrypt(message.encode(), public_other))
        print("You: " + message)


def receive_message(client_user):
    while True:
        print("Other: " + rsa.decrypt(client_user.recv(1024), private_key).decode())


threading.Thread(target=send_message, args=(client,)).start()
threading.Thread(target=receive_message, args=(client,)).start()
