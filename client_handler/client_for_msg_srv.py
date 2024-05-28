import socket

from client_handler.cypher import encrypt_authenticator, encrypt_msg
from client_handler.file_handler import get_msg_server_ip_and_port
from client_handler.request_handler import send_req_get_res, req1028, req1029


def client_for_msg_srv(client_id, ticket, key):
    try:
        host, port = get_msg_server_ip_and_port("srv.info")
        if not host or not port:
            print("Server IP or port not found.")
            return False

        with socket.socket() as client_socket:
            client_socket.connect((host, port))
            print("Connected to msg server successfully.")

            authenticator = encrypt_authenticator(key, client_id)

            msg_header, msg_payload = req1028(client_id, authenticator, ticket)

            print("sending authenticator and ticket to the msg server")
            header, payload = send_req_get_res(client_socket, msg_header, msg_payload)

            if header[1] == 1609:
                print("message server responded with an error")
                exit(1)

            if header[1] == 1604:
                print("message server got the symmetric key")

            while True:
                print("To exit the message server enter: EXIT")
                message_content = input("Please enter the message you want to send:\n")
                if len(message_content) > 2**32 - 1:
                    print("The message is too long. please provide a message in length than 2**32")
                    continue

                message_content = message_content.encode()
                encrypted_message = encrypt_msg(key, message_content)
                message_size = encrypted_message[0]
                message_iv = encrypted_message[1]
                encrypted_content = encrypted_message[2]

                msg_header, msg_payload = req1029(client_id, message_size, message_iv, encrypted_content)

                header, payload = send_req_get_res(client_socket, msg_header, msg_payload)

                if header[1] == 1609:
                    print("msg server responded with general error")
                    exit(1)
                if header[1] == 1605:
                    print("msg server got the message and says thank you")
                if message_content.decode() == 'EXIT':
                    break

    except FileNotFoundError:
        print("Configuration file 'srv.info' not found.")
    except socket.gaierror:
        print("Address-related error connecting to server.")
    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print("Closing the connection with the msg server")


if __name__ == '__main__':
    pass
