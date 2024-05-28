import hashlib
import uuid
import os


def generate_uuid(path_to_clients):
    print("generating new UUID")
    generated_uuid = uuid.uuid4()
    formatted_uuid = generated_uuid.hex

    if check_uuid_in_clients(formatted_uuid, path_to_clients) is False:
        return generate_uuid(path_to_clients)
    return formatted_uuid


def generate_aes_key():
    key = os.urandom(32)  # AES-256 bit key


def string_to_sha256(input_string):
    encoded_string = input_string.encode()
    sha256_hash = hashlib.sha256()
    sha256_hash.update(encoded_string)
    return sha256_hash.hexdigest()


def check_name_in_clients(client_name, path_to_clients):
    try:
        with open(path_to_clients) as file:
            for line in file:
                client_info = line.strip().split(':')
                if client_info[1] == client_name:
                    print("Error: The given name is already exists in clients folder")
                    return False
            return True
    except FileNotFoundError:
        print(f"The file {path_to_clients} was not found.")
    except PermissionError:
        print(f"Permission denied when trying to read {path_to_clients}.")
    except Exception as e:
        print(f"An error occurred: {e}")


def check_uuid_in_clients(client_id, path_to_clients):
    try:
        with open(path_to_clients) as file:
            for line in file:
                client_info = line.strip().split(':')
                if client_info[0] == client_id:
                    print("Error: The given uuid is already exists in clients folder")
                    return False
            return True
    except FileNotFoundError:
        print(f"The file {path_to_clients} was not found.")
    except PermissionError:
        print(f"Permission denied when trying to read {path_to_clients}.")
    except Exception as e:
        print(f"An error occurred: {e}")


def add_client_to_clients(client_id, name, password_hash, last_seen, path_to_clients):
    try:
        with open(path_to_clients, 'a') as file:
            line = client_id + ':' + name + ':' + password_hash + ':' + last_seen + '\n'
            file.write(line)
            return True
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
        return False

