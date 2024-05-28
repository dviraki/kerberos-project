import struct


def req_to_server(client_id, client_version, code, payload_size, payload):
    header = struct.pack('<16sBHI', client_id, client_version, code, payload_size)
    return header, payload


# Request to sign in to the auth server - 1024
def req1024(name, password):
    payload = (name + password).encode('utf-8')
    payload_size = len(payload)
    return req_to_server(b'\0' * 16, 24, 1024, payload_size, payload)


# Request for symmetric key to the auth server - 1027
def req1027(client_id, nonce, server_id=b'\0'*16,):
    payload = server_id + nonce
    payload_size = len(payload)  # server_id is 16 bytes and nonce is 8 bytes
    return req_to_server(client_id, 24, 1027, payload_size, payload)


# Request for sending symmetric key to the msg server - 1028
def req1028(client_id, authenticator, ticket):
    payload = authenticator + ticket
    payload_size = len(payload)
    return req_to_server(client_id, 24, 1028, payload_size, payload)


# Request for sending message to the msg server - 1029
def req1029(client_id, message_size, message_iv, message_content):
    payload = message_size + message_iv + message_content
    payload_size = len(payload)
    return req_to_server(client_id, 24, 1029, payload_size, payload)


def send_req_get_res(client_socket, msg_header, msg_payload):
    try:
        print(f"sending header to server")
        client_socket.send(msg_header)

        print(f"sending payload to server")
        client_socket.send(msg_payload)

        # get the response from the server
        data = client_socket.recv(23)  # receive header server
        if not data:
            print(f"server disconnected")
            exit(1)

        header = struct.unpack('<BHI', data)
        print(f"server responded with the code: {header[1]}")

        if header[0] != 24:
            print(f"server responded with version that in not 24")
            exit(1)

        data = client_socket.recv(header[-1])  # receive payload server
        if not data and header[1] != 1601 and header[1] != 1604 and header[1] != 1605 and header[1] != 1609:
            print(f"server disconnected")
            exit(1)
        # print(f"receiving payload response from server: {data}")
        payload = data

        return header, payload

    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
