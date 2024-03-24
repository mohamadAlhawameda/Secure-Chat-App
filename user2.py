import socket
import os
import threading
from cryptography.fernet import Fernet

# Function to send messages
def send_message(client_socket):
    while True:
        message = input("User 2: ")
        if message == "END CHAT":
            encrypted_message = cipher_suite.encrypt(message.encode())
            client_socket.send(encrypted_message)
            break
        encrypted_message = cipher_suite.encrypt(message.encode())
        client_socket.send(encrypted_message)

# Function to receive and print messages from User1
def receive_message(client_socket, cipher_suite):
    while True:
        encrypted_message = client_socket.recv(1024)
        if not encrypted_message:
            break
        message = cipher_suite.decrypt(encrypted_message).decode()
        if message == "END CHAT":
            print("User 1 has ended the chat.")
            break
        print(' ')
        print("User 1: " + message)

# Create a socket
server_ip = socket.gethostbyname(socket.gethostname())  # Replace with the server's IP address
server_port = 5000  # Replace with the server's port

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Receive the symmetric key from the server
key = client_socket.recv(1024)
cipher_suite = Fernet(key)

# Start send and receive threads
send_thread = threading.Thread(target=send_message, args=(client_socket,))
receive_thread = threading.Thread(target=receive_message, args=(client_socket, cipher_suite))

# Start the threads
send_thread.start()
receive_thread.start()
