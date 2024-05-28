import struct

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad, pad
from datetime import datetime


def decrypt_data(iv, encrypted_data, key):
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(encrypted_data)
        original_data = unpad(decrypted_data, AES.block_size)
        return original_data
    except ValueError:
        print("Incorrect decryption or padding.")
        return False


def encrypt_authenticator(key, client_id, srv_id=b'\0'*16, srv_ver=b'\x18'):
    try:
        creation_time = int(datetime.now().timestamp())
        creation_time_bytes = struct.pack('<Q', creation_time)
    except Exception as e:
        print(f"Error with datetime operation: {e}")
        return False

    iv = get_random_bytes(16)
    data = srv_ver + client_id + srv_id + creation_time_bytes
    data_to_encrypt = pad(data, AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(data_to_encrypt)

    return iv + encrypted_data


def encrypt_msg(key, message):

    iv = get_random_bytes(16)
    data = message
    data_to_encrypt = pad(data, AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(data_to_encrypt)

    length_in_bytes = len(encrypted_data).to_bytes(4, byteorder='little')

    return [length_in_bytes, iv, encrypted_data]


if __name__ == '__main__':
    pass
