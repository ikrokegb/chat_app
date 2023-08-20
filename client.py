import socket
import threading


nickname = input('choose a nickname: ')


client = socket.socket(socket.AF_NET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))

def receive():
    while 1:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'POLLY':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print('An error occurred')
            client.close()
            break



def write():
    while 1:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
