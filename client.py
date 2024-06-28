import socket
import threading

SERVER_IP = "172.22.230.10"
SERVER_PORT = 12000
BUFFER_SIZE = 1024


def receive_message(client_socket):
    while True:
        try:
            message, _ = client_socket.recvfrom(BUFFER_SIZE)
            print(f"\n{message.decode('utf-8')}")
        except:
            pass


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    receive_thread = threading.Thread(target=receive_message, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        message = message
        if message:
            client_socket.sendto(message.encode('utf-8'), (SERVER_IP, SERVER_PORT))


if __name__ == "__main__":
    main()
