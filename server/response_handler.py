import struct


def res_to_client(server_version, code, payload_size, payload):
    header = struct.pack('<BHI', server_version, code, payload_size)
    return header, payload


# Response for sign in to the auth server. Success - 1600
def res1600(client_id):
    payload = client_id
    payload_size = len(payload)
    return res_to_client(24, 1600, payload_size, payload)


# Response for sign in to the auth server. Failed - 1601
def res1601():
    return res_to_client(24, 1601, 0, b'')


# Response for sending encrypted symmetric key - 1603
def res1603(client_id, encrypted_key, ticket):
    payload = (client_id + encrypted_key + ticket)
    payload_size = len(payload)
    return res_to_client(24, 1603, payload_size, payload)


# Response for a general server error that was not handled in one of the previous cases. - 1609
def res1609():
    return res_to_client(24, 1609, 0, b'')


# Response for confirming receiving a symmetric key - 1604
def res1604():
    return res_to_client(24, 1604, 0, b'')


# Response for confirming receiving a message, thank you - 1605
def res1605():
    return res_to_client(24, 1605, 0, b'')


def get_req_from_client(conn, client_num):
    try:
        data = conn.recv(23)  # header is 23 bytes
        if not data:
            print(f"Client number {client_num} has disconnected")
            exit(1)
        msg_header = struct.unpack('<16sBHI', data)
        print(f"The header was received from client number: {client_num} with the code: {msg_header[2]}")
        data = conn.recv(msg_header[-1])  # msg_header[-1] is the payload size
        if not data:
            print(f"Client number {client_num} has disconnected")
            exit(1)
        print(f"The payload was received from client number {client_num}")
        msg_payload = data

        return msg_header, msg_payload

    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

