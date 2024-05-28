import os
import re


def check_me_info_file(file_path):
    try:
        with open(file_path) as info:
            lines = info.read().split('\n')

            if len(lines) != 2:
                print("Error: the format of me.info needs to be two lines.")
                return False

            name = lines[0]
            unique_id = lines[1]

            if len(name) > 255:
                print("Error: name can be up to 255 bytes in me.info file.")
                return False

            # Check unique ID pattern (32 hexadecimal characters)
            if not re.match(r'^[a-f0-9]{32}$', unique_id):
                print("Error: unique ID format is incorrect in me.info file.")
                return False

            return name, unique_id
    except FileNotFoundError:
        print("Error: The specified file was not found.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def make_me_info_file(file_path, client_name, client_id):
    try:
        with open(file_path, 'w') as file:
            file.write(f"{client_name}\n{client_id}")
        print(f"File has been created and written to at: {file_path}")
    except Exception as e:
        print(f"An error occurred while creating or writing to the file: {e}")


def read_me_info_file(file_path):
    try:
        with open(file_path, 'r') as file:
            name = file.readline().strip('\n')
            uuid = file.readline().strip('\n')
            return name, uuid
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")


def get_auth_server_ip_and_port(file_path):
    return get_server_ip_and_port(file_path)[0]


def get_msg_server_ip_and_port(file_path):
    return get_server_ip_and_port(file_path)[1]


def get_server_ip_and_port(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.read().split('\n')

            if len(lines) != 2:
                print("Error: the format of me.info needs to be two lines.")
                return False

            # Read the first two lines from the file
            auth_server_line = lines[0].strip()
            msg_server_line = lines[1].strip()

            # Split each line to separate IP and port
            auth_server_ip, auth_server_port = auth_server_line.split(':')
            msg_server_ip, msg_server_port = msg_server_line.split(':')

            # Convert port numbers to integers
            auth_server_port = int(auth_server_port)
            msg_server_port = int(msg_server_port)

            return (auth_server_ip, auth_server_port), (msg_server_ip, msg_server_port)
    except FileNotFoundError:
        print("Error: The specified file was not found.")
        return False
    except ValueError:
        print("Error: Invalid format in file.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def find_me_info_file():
    dir_list = os.listdir()
    for file_path in dir_list:
        if file_path[-7:] == "me.info":
            return True
    print("The file me.info is not in the file path.")
    return False


if __name__ == '__main__':
    x = get_server_ip_and_port('srv.info')
    print(x)
