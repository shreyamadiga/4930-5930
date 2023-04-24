# Here are our imports for the project
# Socket is used to setup our local server for hosting
# and it allows for a connection between the "2 users"
# Threading is used to allow for our machine to run two concurrent threads
# of this program. One will be used for sending messages and the other for
# receiving messages.
# The RSA import allows us to encrypt our messages using the rsa enctryption algorithm
import socket
import threading
import rsa

# This will create a public_key and a private key of size 1024
# The other public key will be created upon connection
public_key, private_key = rsa.newkeys(1024)
public_other = None

# This will prompt the user for selection of hosting the session
# or connecting to a session
choice = input("Do you want to host (1) or to connect (2): ")

# If user selects "1", a socket stream will be created and bound with our private IP address
# and port 9999. Then we will tell the server to listen for any incoming connections.
# When the client connects, the hosts public_key is sent to client, and the clients public key
# is set when it receives it from the host
if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Change to your current IP address
    server.bind(("10.0.0.41", 9999))
    server.listen()

    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_other = rsa.PublicKey.load_pkcs1(client.recv(1024))
# If use selects "2", they will be connected to the host session if one exists. The user will be bound
# to the socket using their IP and port 9999. We then also ensure the other users' public key is set
# to that of the hosts so that the private key can be used later for decryption
elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Change to your current IP address, must match IP in choice 1
    client.connect(("10.0.0.41", 9999))
    public_other = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))
# Stop program otherwise
else:
    exit()

# Send message method and receive message methods used to encrypt and decrypt the
# sent messages


def send_message(client_user):
    while True:
        message = input("")
        encrypted_message = rsa.encrypt(message.encode(), public_other)
        print("Your Plain-Text Message: " + message)
        # uncomment the line below this to show encrypted message in the output
        # used to verify the message was encrypted
        # print("Your Encrypted Message: " + encrypted_message.hex())
        client_user.send(encrypted_message)


def receive_message(client_user):
    while True:
        print("Other (Decrypted message): " + rsa.decrypt(client_user.recv(1024), private_key).decode())


# These threads allow us to send and receive messages concurrently using their own
# threads
threading.Thread(target=send_message, args=(client,)).start()
threading.Thread(target=receive_message, args=(client,)).start()
