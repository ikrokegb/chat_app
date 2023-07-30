import socket
import threading

HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5

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

if __name__ == "__main__":
    main()