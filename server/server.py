import socket
import threading

HOST = '0.0.0.0'
# HOST = '127.0.0.1'
PORT = 12345


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
aliases = []


# Broadcast message to all clients
def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            client.send(message)


# Handle client communication
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except Exception as e:
            print(e)
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat!'.encode('utf-8'))
            aliases.remove(alias)
            break


# Receive clients and start handling their messages
def receive():
    while True:
        client, address = server.accept()
        print(f'Connection established with {address}')

        client.send('ALIAS'.encode('utf-8'))
        alias = client.recv(1024).decode('utf-8')
        aliases.append(alias)
        clients.append(client)

        print(f'The alias of this client is {alias}')
        broadcast(f'{alias} has joined the chat!'.encode('utf-8'), client)
        client.send('You are now connected!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


print('Server is listening...')
receive()
