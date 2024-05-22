import socket
import threading
import os
import time

# Define server host and port
HOST = 'server'  # Service name defined in docker-compose.yml
# HOST = 'localhost'  # Localhost
PORT = 12345     # Port to connect to

alias = os.getenv('ALIAS', 'anonymous')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Attempt to connect to the server with retries
connected = False
while not connected:
    try:
        client.connect((HOST, PORT))
        connected = True
    except ConnectionRefusedError:
        print("Connection refused, retrying in 5 seconds...")
        time.sleep(5)


# Listen for messages from the server
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'ALIAS':
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except Exception as e:
            print(e)
            print('Error!')
            client.close()
            break


# Send messages to the server
def send_messages():
    while True:
        message = f'{input("")}'
        client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
