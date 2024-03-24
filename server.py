import socket
import threading
from cryptography.fernet import Fernet

# Generate a symmetric key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Function to handle client connections
def handle_client(client_socket, client_address, user):
    print(f"Accepted connection from {client_address}")

    # Send the symmetric key to the client
    client_socket.send(key)

    # Open a separate chat log file for each user
    chat_log_file = open(f"encrypted_chat_log_{user}.txt", "ab")  # Open the chat log file for appending in binary mode

    try:
        while True:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break

            # Decrypt the message using the symmetric key
            message = cipher_suite.decrypt(encrypted_message).decode()

            if message == "END CHAT":
                print(f"{user} has ended the chat.")
                break

            print(' ')
            print(f"{user} (Encrypted): {encrypted_message.hex()}")
            print(f"{user} (Decrypted): {message}")
            print(' ')

            # Format and write the messages in the chat log file
            chat_log_file.write(f"{user} (Encrypted): {encrypted_message.hex()}\n".encode())
            chat_log_file.write(f"{user} (Decrypted): {message}\n".encode())
            chat_log_file.flush()  # Ensure the messages are immediately written to the file

            # Relay the decrypted message to all connected clients (except the sender)
            for client in clients:
                if client != client_socket:
                    try:
                        client.send(encrypted_message)
                    except Exception as e:
                        print(f"Error sending message to {client.getpeername()}: {e}")

    except Exception as e:
        print(f"Error handling connection from {client_address}: {e}")

    client_socket.close()
    chat_log_file.close()  # Close the chat log file
    print(f"Connection from {client_address} closed.")

# Create a socket
server_ip = socket.gethostbyname(socket.gethostname())  # Replace with the server's IP address
server_port = 5000  # Replace with the server's port

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(5)  # Listen for up to 5 connections

print(f"Server listening on {server_ip}:{server_port}")

clients = []

while True:
    try:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)

        if len(clients) == 1:
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, "User 1"))
        else:
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, "User 2"))
    
        client_thread.start()
    except Exception as e:
        print(f"Error accepting connection: {e}")
