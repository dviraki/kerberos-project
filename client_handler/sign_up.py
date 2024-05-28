import hashlib


def get_client_name_and_pass():
    while True:
        name = input("Please provide name with max length up to 254 bytes\n")
        if len(name) < 255:
            name += '\0'
            break
        else:
            print("Error: please provide a name with less than 255 characters and ascii characters")

    while True:
        password = input("Please provide password with max length up to 254 bytes\n")
        if len(password) < 255:
            password += '\0'
            break
        else:
            print("Error: please provide a password with less than 255 characters and ascii characters")

    return name, password


def get_client_pass_hash():
    while True:
        password = input("Please provide password with max length up to 254 bytes\n")
        if len(password) < 255:
            break
        else:
            print("Error: please provide a password with less than 255 characters and ascii characters")
    return string_to_sha256(password)


def string_to_sha256(input_string):
    encoded_string = input_string.encode()
    sha256_hash = hashlib.sha256()
    sha256_hash.update(encoded_string)
    return sha256_hash.digest()  # Return the hash in byte form
