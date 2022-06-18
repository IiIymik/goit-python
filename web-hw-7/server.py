import socket
import threading


def print_info(data, addr):
    print(addr, str(data))


def send_messega(socket_server, clients, addr, data):
    if len(clients) != 0:
        for client in clients:
            if client != addr:
                socket_server.sendto((addr[0] + ":" + str(addr[1])+" ").encode()+data, (client))


def listen_socket(socket_server, clients, conn, addr):
    data = conn
    print_info(data, addr)
    send_messega(socket_server, clients, addr, data)


def main():

    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 9000

    print(f"HOST:{HOST} PORT:{PORT}")

    socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_server.bind((HOST, PORT))
    socket_server.setblocking(10)

    print("Started server")

    clients = list()

    while True:
        try:
            conn, addr = socket_server.recvfrom(1024)

            if addr not in clients:
                clients.append(addr)
                print("Connected by", addr)
                threading.Thread(target=listen_socket, args=(socket_server, clients, conn, addr)).start()

        except ConnectionResetError:
            print("The remote host forcibly dropped the existing connection")
        except KeyboardInterrupt:
            print("Stopped server")


if __name__ == '__main__':
    main()