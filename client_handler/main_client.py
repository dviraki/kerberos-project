from client_handler.client_for_auth_srv import client_for_auth_srv
from client_handler.client_for_msg_srv import client_for_msg_srv


def main():
    client_id_bytes, ticket, key = client_for_auth_srv()
    client_for_msg_srv(client_id_bytes, ticket, key)


if __name__ == '__main__':
    main()
