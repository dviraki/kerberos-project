from server.make_server import make_server
from server.response_handler import get_req_from_client, res1609, res1605, res1604
from server.utils import read_port_from_file, decrypt_message, read_key_from_msg_info, update_last_seen


def threaded_client_msg_srv(conn, client_num):
    aes_key = None
    while True:
        try:
            header, payload = get_req_from_client(conn, client_num)
            client_id = header[0]
            code_client = header[2]
            client_info = update_last_seen(client_id.hex(), "clients")

            if code_client == 1028:
                auth = payload[:64]
                ticket = payload[64:]

                auth_iv = auth[:16]
                ticket_iv = ticket[41:57]

                enc_auth = auth[16:]
                enc_ticket = ticket[57:]

                msg_key = read_key_from_msg_info("msg.info")
                dec_ticket = decrypt_message(ticket_iv, enc_ticket, msg_key)

                aes_key = dec_ticket[:32]
                dec_auth = decrypt_message(auth_iv, enc_auth, aes_key)

                print(f"sending to client number {client_num} that msg server got the symetric key")
                res_header, res_payload = res1604()
                conn.send(res_header)
                conn.send(res_payload)
                continue

            if code_client == 1029 and aes_key is not None:
                msg_iv = payload[4:20]
                msg_content = payload[20:]
                original_msg = decrypt_message(msg_iv, msg_content, aes_key)
                print(f"client sent the message: {original_msg.decode()}")
                print(f"sending to client 'thank you' and that server got the message")
                res_header, res_payload = res1605()
                conn.send(res_header)
                conn.send(res_payload)
                continue
            else:
                print("unrecognized code was sent by the client")
                res_header, res_payload = res1609()
                conn.send(res_header)
                conn.send(res_payload)
                continue

        except Exception as e:
            print(f"An error occurred: {e}")
            res_header, res_payload = res1609()
            conn.send(res_header)
            conn.send(res_payload)
            break

    conn.close()
    print(f"client {client_num} disconnected")


if __name__ == '__main__':
    port = read_port_from_file("port.info")
    print("making msg server")
    make_server(port + 1, threaded_client_msg_srv)
