import struct
import base64
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def read_port_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            port_str = file.read().strip()
            port = int(port_str)
            if 1 <= port <= 65535:
                return port
            else:
                print(f"Port number in the file ({port}) is not valid. Using default port 1256.")
                return 1256
    except FileNotFoundError:
        print(f"File not found. Using default port 1256.")
        return 1256
    except ValueError:
        print(f"Invalid content in file. Using default port 1256.")
        return 1256
    except OSError as e:
        print(f"Error opening file: {e}. Using default port 1256.")
        return 1256


def read_key_from_msg_info(path_to_msg_info):
    try:
        with open(path_to_msg_info) as file:
            content = file.readlines()
            if len(content) < 4:
                print("The file does not contain enough lines.")
                return False
            msg_srv_key = base64.b64decode(content[3].strip())
            return msg_srv_key
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def update_last_seen(uuid, path_to_file):
    client_info = []

    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    except Exception as e:
        print(f"Error with datetime operation: {e}")
        return False

    lines = []
    updated = False

    try:
        with open(path_to_file, 'r') as file:
            for line in file:
                client_info = parts = line.strip().split(':')
                if parts[0] == uuid:
                    parts[-1] = current_time
                    line = ':'.join(parts) + '\n'
                    updated = True
                lines.append(line)
    except FileNotFoundError:
        print(f"File {path_to_file} not found.")
        return False
    except IOError as e:
        print(f"Error reading file {path_to_file}: {e}")
        return False

    if updated:
        try:
            with open(path_to_file, 'w') as file:
                file.writelines(lines)
        except IOError as e:
            print(f"Error writing to file {path_to_file}: {e}")
            return False
    return client_info


def generate_32_byte_key():
    return get_random_bytes(32)


def encrypt_key_to_client(nonce, pass_hash, aes_key):
    iv = get_random_bytes(16)
    data = nonce + aes_key
    data_to_encrypt = pad(data, AES.block_size)
    cipher = AES.new(pass_hash, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(data_to_encrypt)

    return iv + encrypted_data


def encrypt_ticket(client_id, path_to_msg_info, aes_key, srv_ver=b'\x18', srv_id=b'\0'*16):
    try:
        unix_timestamp = int(datetime.now().timestamp())
        creation_time = unix_timestamp
        expiration_time = unix_timestamp + 60 * 5  # expiration will be 5 minutes from created time
        creation_time_bytes = struct.pack('<Q', unix_timestamp)
        expiration_time_bytes = struct.pack('<Q', expiration_time)
    except Exception as e:
        print(f"Error with datetime operation: {e}")
        return False

    msg_srv_key = read_key_from_msg_info(path_to_msg_info)
    if msg_srv_key is False:
        return False

    iv = get_random_bytes(16)
    data = aes_key + expiration_time_bytes
    data_to_encrypt = pad(data, AES.block_size)
    cipher = AES.new(msg_srv_key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(data_to_encrypt)

    return srv_ver + client_id + srv_id + creation_time_bytes + iv + encrypted_data


def decrypt_message(msg_iv, msg_content, key):
    cipher = AES.new(key, AES.MODE_CBC, msg_iv)

    decrypted_data = cipher.decrypt(msg_content)

    try:
        original_msg = unpad(decrypted_data, AES.block_size)
    except ValueError:
        print("Incorrect decryption or padding.")
        return False

    return original_msg


if __name__ == '__main__':
    pass

