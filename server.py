import socket
import threading

HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = [] #connected users


def listen_for_messages(client, username):
    message = client.recv(2048).decode('utf-8') # listen messeges
    if message != '':
        final_message = username + '~' + message #name~mes
        send_messages_to_all(final_message)
    else:
        print(f'The message from client {username} is empty')


def send_message_to_client(message): #for one client
    pass


def send_messages_to_all(message):
    pass


def client_handler(client):
    while 1:
        username = client.recv(2048).decode('utf-8') # listen username
        if username != '':
            active_clients.append((username, client))
        else:
            print('Client username is empty')


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #1 - IPv4    2 - TCP

    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except socket.error as e:
        print(e)
        #print(f'Unable to bind to host {HOST} and port {PORT} ')

    server.listen(LISTENER_LIMIT)

    while 1:
        client, adress = server.accept()
        print(f"Succesfully connected to client {adress[0]}, {adress[1]}")
        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == "__main__":
    main()