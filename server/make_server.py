import socket
from _thread import *


def make_server(port_from_file, threaded_program):
    host = "10.0.0.4"  # socket.gethostname()
    port = port_from_file
    MAX_CLIENTS = 5
    clients = {}
    client_num = 0
    server_str = str(host)

    server_socket = socket.socket()

    try:
        server_socket.bind((host, port))
    except socket.error as e:
        str(e)

    # configure how many client_handler the server can listen simultaneously
    server_socket.listen(MAX_CLIENTS)

    print("Waiting for a connection, Server Started")
    print('server: ' + str(server_str))
    print('port: ' + str(port))

    while True:
        try:
            conn, addr = server_socket.accept()
        except Exception as e:
            print(f"server_socket.accept failed: {str(e)}")
            print('exiting make server function')
            return

        print(f"{conn} is connected to: {addr}")

        clients[client_num] = conn  # adding the client_handler to the client_handler dictionary
        start_new_thread(threaded_program, (conn, client_num))
        client_num += 1
