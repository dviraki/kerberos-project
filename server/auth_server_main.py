from server.make_server import make_server
from server.registration_handler import check_name_in_clients, generate_uuid, add_client_to_clients, string_to_sha256
from server.response_handler import res1601, res1600, res1603, res1609, get_req_from_client
from utils import update_last_seen, encrypt_key_to_client, generate_32_byte_key, encrypt_ticket, read_port_from_file


def threaded_client_auth_srv(conn, client_num):
    while True:
        try:
            msg_header, msg_payload = get_req_from_client(conn, client_num)
            client_id = msg_header[0]
            code_client = msg_header[2]
            try:
                msg_payload = msg_payload.decode('utf-8')
            except:
                pass

            # If client request for registration and the client name is already in the database
            if code_client == 1024 and check_name_in_clients(msg_payload.split('\0')[0], "clients") is False:
                res_header, res_payload = res1601()
                conn.send(res_header)
                conn.send(res_payload)
                continue

            # If registration from client is a success then send UUID
            if code_client == 1024 and check_name_in_clients(msg_payload.split('\0')[0], "clients") is True:
                client_id = generate_uuid("clients")
                client_pass_hash = string_to_sha256(msg_payload.split('\0')[1])
                client_name = msg_payload.split('\0')[0]
                if add_client_to_clients(client_id, client_name, client_pass_hash, "last_seen_temp", "clients"):
                    update_last_seen(client_id, "clients")
                else:
                    print("An error occurred when adding client to clients file")
                    break
                res_header, res_payload = res1600(bytes.fromhex(client_id))
                conn.send(res_header)
                conn.send(res_payload)
                continue

            if code_client == 1027:
                client_info = update_last_seen(client_id.hex(), "clients")
                pass_hash = bytes.fromhex(client_info[2])
                if not client_info:
                    print("server responded with error")
                    break
                client_nonce = msg_payload[16:]
                # send AES key
                aes_key = generate_32_byte_key()

                encrypted_key = encrypt_key_to_client(client_nonce, pass_hash, aes_key)
                print(f"{client_id}\n{client_nonce}\n{encrypted_key}")
                encrypted_ticket = encrypt_ticket(client_id, "msg.info", aes_key)

                if encrypted_ticket is False:
                    print("server responded with error")
                    break
                res_header, res_payload = res1603(client_id, encrypted_key, encrypted_ticket)
                conn.send(res_header)
                conn.send(res_payload)
                continue
            else:
                print("Error occurred when client sent data")
                update_last_seen(client_id.hex(), "clients")
                res_header, res_payload = res1609()
                conn.send(res_header)
                conn.send(res_payload)
                continue

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    conn.close()
    print(f"client {client_num} disconnected")


if __name__ == '__main__':
    port = read_port_from_file("port.info")
    print("making auth server")
    make_server(port, threaded_client_auth_srv)
