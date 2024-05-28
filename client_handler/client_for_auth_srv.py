import socket

from Crypto.Random import get_random_bytes

from client_handler.cypher import decrypt_data
from client_handler.sign_up import get_client_name_and_pass, get_client_pass_hash
from client_handler.file_handler import find_me_info_file, check_me_info_file, \
    get_auth_server_ip_and_port, make_me_info_file, read_me_info_file
from client_handler.request_handler import req1024, req1027, send_req_get_res


def client_for_auth_srv():
    first_time_signing_up = False

    if not find_me_info_file():
        first_time_signing_up = True

    try:
        host, port = get_auth_server_ip_and_port("srv.info")
        if not host or not port:
            print("Server IP or port not found.")
            exit(1)

        with socket.socket() as client_socket:
            client_socket.connect((host, port))
            print("Connected to auth server successfully.")

            while first_time_signing_up:
                print("signing in to the auth server")
                name, password = get_client_name_and_pass()
                msg_header, msg_payload = req1024(name, password)

                header, payload = send_req_get_res(client_socket, msg_header, msg_payload)

                if header[1] == 1600:
                    # make me.info file and save the name and the unique ID
                    print("making me.info and saving the name and the unique ID")
                    unique_id = payload.hex()
                    make_me_info_file("me.info", name[:-1], unique_id)
                elif header[1] == 1601:
                    print("registration failed")
                    continue

                first_time_signing_up = False

            # read from me.info file the name and unique id to reconnect
            if check_me_info_file("me.info") is False:
                print("error with me.info file")
                exit(1)

            name, unique_id = read_me_info_file("me.info")

            # request key
            print("requesting encrypted key for the msg server")
            nonce = get_random_bytes(8)

            msg_header, msg_payload = req1027(bytes.fromhex(unique_id), nonce)

            header, payload = send_req_get_res(client_socket, msg_header, msg_payload)

            encrypted_key = payload[16:80]
            enc_key_iv = encrypted_key[:16]
            enc_key_nonce_and_aes = encrypted_key[16:]

            encrypted_ticket = payload[80:]

            while True:
                pass_hash = get_client_pass_hash()
                dec_nonce_and_key = decrypt_data(enc_key_iv, enc_key_nonce_and_aes, pass_hash)
                if dec_nonce_and_key is not False and dec_nonce_and_key[:8] == nonce:
                    print("The password you entered is correct")
                    break
                print("The password you entered is incorrect")

            dec_nonce = dec_nonce_and_key[:8]
            dec_key = dec_nonce_and_key[8:]

            print("Client got the secret key for the msg server")

    except FileNotFoundError:
        print("Configuration file 'srv.info' not found.")
    except socket.gaierror:
        print("Address-related error connecting to server.")
    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print("Closing the connection with the auth server\n")

    return bytes.fromhex(unique_id), encrypted_ticket, dec_key


if __name__ == '__main__':
    client_for_auth_srv()

