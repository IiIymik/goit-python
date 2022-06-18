import socket
import threading
import time
import sys


def send(client_socket, message, server):
    client_socket.sendto(message, server)


def recv_massage(client_socket):
    while True:
        try:
            data, addr = client_socket.recvfrom(1024)
            print(data.decode("utf-8"))
            time.sleep(0.2)
        except OSError:
            break
        except ConnectionResetError:
            print("Server is down or no data\nPlease check if the server is enabled\nTry again")
            client_socket.close()
            break


def main():
    SERVER = (socket.gethostbyname(socket.gethostname()), 9000)
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 0
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind((HOST, PORT))
    while True:
        connection = input("Connect to server? Y/N ")
        if connection.casefold() == "y":
            client_socket.sendto(b"Connect", SERVER)
            break
        elif connection.casefold() == "n":
            sys.exit(0)
        else:
            continue

    thread_recv = threading.Thread(target=recv_massage, args=(client_socket,))
    thread_recv.start()

    while True:
        try:
            message = input().encode()
            if len(message) > 0:
                send(client_socket=client_socket, message=message, server=SERVER)
            time.sleep(0.2)
        except KeyboardInterrupt:
            print("Exit")
            client_socket.sendto(b"Disconnect", SERVER)
            client_socket.close()
            break
        except (ConnectionAbortedError, ConnectionError, ConnectionRefusedError, ConnectionResetError, OSError):
            print("Exit")
            client_socket.close()
            break

if __name__ == "__main__":
    main()