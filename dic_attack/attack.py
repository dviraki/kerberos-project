import ast
import hashlib

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def decrypt_content(iv, content, key):
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(content)
        original_msg = unpad(decrypted_data, AES.block_size)
        return original_msg
    except Exception as e:
        return None


def string_to_sha256(input_string):
    encoded_string = input_string.encode()
    sha256_hash = hashlib.sha256()
    sha256_hash.update(encoded_string)
    return sha256_hash.hexdigest()


# this is the format in the users file client_id:client_nonce:encrypted_key
# the encrypted_key has 16 bytes of iv and then the encrypted key data
def get_user_info(user):
    client_id = user[0].hex()
    nonce = user[1]
    iv = user[2][:16]
    encrypted_aes_key = user[2][16:]
    return [client_id, nonce, iv, encrypted_aes_key]


def hash_password(password):
    encoded_string = password.encode()
    sha256_hash = hashlib.sha256()
    sha256_hash.update(encoded_string)
    return sha256_hash.digest()


def load_users(path_to_users):
    users = []
    with open(path_to_users, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            # Convert the string representation to actual bytes
            client_id_bytes = ast.literal_eval(lines[i].strip())
            client_nonce_bytes = ast.literal_eval(lines[i + 1].strip())
            encrypted_bytes = ast.literal_eval(lines[i + 2].strip())
            users.append([client_id_bytes, client_nonce_bytes, encrypted_bytes])
    return users


def load_passwords(path_to_passwords):
    passwords = []
    with open(path_to_passwords, 'r') as file:
        for line in file:
            passwords.append(line.strip())
    return passwords


def check_pass_for_user(user, password):
    client_id = user[0]
    nonce = user[1]
    iv = user[2]
    enc_nonce_and_key = user[3]
    pass_hash = hash_password(password)

    dec_nonce_and_key = decrypt_content(iv, enc_nonce_and_key, pass_hash)  # nonce is the first 8 bytes
    if dec_nonce_and_key is None:
        return None

    dec_nonce = dec_nonce_and_key[:8]
    dec_key = dec_nonce_and_key[8:]
    if dec_nonce != nonce:
        return None

    return [client_id, dec_key]


def get_user_and_pass_matches(users, passwords):
    user_and_pass_matches = []
    for usr in users:
        user_attributes = get_user_info(usr)
        for pss in passwords:
            match = check_pass_for_user(user_attributes, pss)
            if match is not None:
                user_and_pass_matches.append(match)
                print("THERE IS A MATCH!!!")
                print(f"UUID: {match[0]} PASSWORD: {pss}")
    return user_and_pass_matches


if __name__ == '__main__':
    """
    the format of the users file:
    for each user this is the format:
    
        first line is: client_id
        second line is: client_nonce
        third line is: encrypted_key
     
    every three lines the byte data is associated to one client.
     
    """
    users_path = "users.txt"
    passwords_path = "passwords.txt"

    users_list = load_users(users_path)
    passwords_list = load_passwords(passwords_path)

    matches = get_user_and_pass_matches(users_list, passwords_list)






