#   Athavan Jesunesan - 6705271


import threading
import socket
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import zlib

# Static Requirements
IP = "127.0.0.1"
PORT = 1234
FORMAT = 'utf-8'
HEADER = 64
MENU = 'What method would you like to use: \n (1): Encryption \n (2): Checksums \n (3) All of the above'
CHOOSE_FILE = 'Please select a number to send: '

#Encryption
password = "supersecret"
salt = b'saltysalt'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))


def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(file_path, key):
    iv = os.urandom(16)  # Generate a random IV for each file
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(file_path, 'rb') as f:
        file_data = f.read()

    encrypted_data = encryptor.update(file_data) + encryptor.finalize()
    return iv + encrypted_data

def calculate_crc32(data):
    return zlib.crc32(data).to_bytes(4, byteorder='big')

# Receive message if there was an issue processing the message (due to too many jobs running on server)
# (f)
def clientRecieve():
    while True:
        messageLength = client.recv(HEADER).decode(FORMAT)
        if messageLength:
            messageLength = int(messageLength)
            message = client.recv(messageLength).decode(FORMAT)
            print(message)

def clientSend():
    print('Welcome to the File transfer system!')

    while True:

        # Setup
        print(MENU)
        choice = input('Select an option: ')
        print(CHOOSE_FILE)

        # Ensures the chosen files exists
        file = '0'
        while int(file) < 1 or int(file) > 20:
            file = input('Choose from 1 to 20: ')

        # Set the file path
        file_path = f'./client_folder/file_{file}.bin'

        # Prepare the server for the service it needs to accomodate
        client.send(choice.encode(FORMAT))

        # Prepare identifiers to send to server
        file_name = f'file_{file}.bin'
        client.send(file_name.encode())
        file_size = os.path.getsize(file_path)
        client.send(str(file_size).encode())

        print(f'You have chosen: {file_path}')
        print(f'This file has a size of {file_size}')

        # Sends file based on choice
        if choice == '1': # Encryption

            key = derive_key(password, salt)
            encrypted_data = encrypt_file(file_path, key)
            client.sendall(encrypted_data)
            print("File sent successfully")
        

        elif choice == '2': # Check Sums

            with open(file_path, 'rb') as f:
                file_data = f.read()
            checksum = calculate_crc32(file_data)
            client.sendall(checksum + file_data)

            print("File sent successfully")
            

        else: # Choice == '3' is the default (Both)

            key = derive_key(password, salt)
            encrypted_data = encrypt_file(file_path, key)
            checksum = calculate_crc32(encrypted_data)
            client.sendall(checksum + encrypted_data)

            print("File sent successfully")


if __name__ == '__main__':       
    threadReceive = threading.Thread(target=clientRecieve)
    threadReceive.start()

    threadSend = threading.Thread(target=clientSend)
    threadSend.start()