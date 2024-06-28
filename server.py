import socket
import threading

SERVER_IP = "172.22.230.10"
SERVER_PORT = 12000
BUFFER_SIZE = 1024

clients = []

def handle_client(server_socket):
    while True:
        try:
            message, client_address = server_socket.recvfrom(BUFFER_SIZE)
            #print(message)

            if client_address not in clients:
                clients.append(client_address)

            print(clients.index(client_address))

            for client in clients:
                if client != client_address:
                    new_message = message.decode('utf-8')
                    id = clients.index(client_address)
                    new_message = str(id) + "#" + new_message
                    server_socket.sendto(new_message.encode('utf-8'), client)
        except:
            pass

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_socket.bind((SERVER_IP, SERVER_PORT))
    print("Server started")

    handle_thread = threading.Thread(target=handle_client, args=(server_socket,))
    handle_thread.start()

if __name__ == "__main__":
    main()