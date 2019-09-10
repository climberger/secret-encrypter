from cryptography.fernet import Fernet
import base64
import os
import sys
import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def create_key():
    key = Fernet.generate_key()
    return key


def write_key_to_file(key, file_name):
    file = open(file_name, 'wb')
    file.write(key)
    file.close()


def get_key_from_file(file_name):
    with open(file_name, 'rb') as key_file:
        key = key_file.read()
    return key


def get_key_from_password(password, salt):
    password_encoded = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password_encoded))
    return key


def create_dalt():
    salt = os.urandom(16)
    return salt


def get_salt_from_file(file_name):
    with open(file_name, 'rb') as file:
        salt = file.read()
    return salt


def write_salt_to_file(salt, file_name):
    file = open(file_name, 'wb')
    file.write(salt)
    file.close()


def encrypt_data(data, key):
    data_bytes = data.encode()
    fernet = Fernet(key)
    data_encrypted = fernet.encrypt(data_bytes)
    return data_encrypted


def decrypt_data(data_encrypted, key):
    data_encrypted_encoded = data_encrypted.encode()
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(data_encrypted_encoded)
    return decrypted_message


def get_dict_from_json_string(json_str):
    json_data = json.loads(json_str)
    return json_data


def get_json_string_from_dict(dict):
    json_str = json.dumps(dict)
    return json_str


def create_store():
    salt = create_dalt()
    write_salt_to_file(salt, 'salt.slt')
    password = input('Choose a password:')
    key = get_key_from_password(password, salt)
    store_dict = {}
    store_store(key, store_dict)


def load_store(key):
    with open('store.enc', 'rb') as f:
        encrypted_store = f.read()
    fernet = Fernet(key)
    decrypted_store = fernet.decrypt(encrypted_store)
    store_json_str = decrypted_store.decode()
    store_dict = get_dict_from_json_string(store_json_str)
    return store_dict


def store_store(key, store_dict):
    json_str = get_json_string_from_dict(store_dict)
    encrypted_store = encrypt_data(json_str, key)
    with open('store.enc', 'wb') as f:
        f.write(encrypted_store)


def set_store_value(name, value):
    salt = get_salt_from_file('salt.slt')
    password = input('Provide password:')
    key = get_key_from_password(password, salt)
    store_dict = load_store(key)
    store_dict[name] = value
    store_store(key, store_dict)


def remove_store_value(name):
    salt = get_salt_from_file('salt.slt')
    password = input('Provide password:')
    key = get_key_from_password(password, salt)
    store_dict = load_store(key)
    del store_dict[name]
    store_store(key, store_dict)


def get_store_value(name):
    salt = get_salt_from_file('salt.slt')
    password = input('Provide password:')
    key = get_key_from_password(password, salt)
    store_dict = load_store(key)
    return store_dict[name]


def get_resource_names():
    salt = get_salt_from_file('salt.slt')
    password = input('Provide password:')
    key = get_key_from_password(password, salt)
    store_dict = load_store(key)
    resource_names = list(store_dict.keys())
    print(resource_names)


def handle_command():
    args = sys.argv
    if len(args) == 2 and args[1] == 'create-store':
        create_store()
    if len(args) == 2 and args[1] == 'list-secrets':
        get_resource_names()
    if len(args) == 3 and args[1] == 'get':
        value = get_store_value(args[2])
        print(value)
    if len(args) == 4 and args[1] == 'set':
        name = args[2]
        value = args[3]
        set_store_value(name, value)
    if len(args) == 3 and args[1] == 'remove':
        remove_store_value(args[2])

# change password
# get content as json
# create store from json

handle_command()
