#   Athavan Jesunesan - 6705271

import threading
import socket
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import hashlib
import zlib

IP = "127.0.0.1"
PORT = 1234
ENCRYPTION = 'sha-256'
FORMAT = 'utf-8'
HEADER = 64
DISCONNECT = "!EXIT"

#Encryption
password = "supersecret"
salt = b'saltysalt'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))


def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def decrypt_file(encrypted_data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted_data

def calculate_crc32(data):
    return zlib.crc32(data)

def verify_checksum(data, received_checksum):
    # Compute the checksum of the received data
    computed_checksum = hashlib.md5(data).hexdigest()
    return computed_checksum == received_checksum

def start(client):

    # Receive file name and size
    choice = client.recv(1).decode()
    #Used for storing the file upon successful transmission
    file_name = client.recv(1024).decode()
    #Ensures that the server can recieve the full file 
    file_size = int(client.recv(1024).decode())
    
    print(f"Receiving file: {file_name}, Size: {file_size} bytes")

    # receives file based on choice
    if choice == '1': # Encryption
        print('The client has chosen to send an encrypted the file... now decrypting.')

        key = derive_key(password, salt)
        with client:
            #Receive the IV and the file
            data = client.recv(16 + file_size)
            iv = data[:16]  # First 16 bytes are the IV
            encrypted_data = data[16:]
            decrypted_data = decrypt_file(encrypted_data, key, iv)

            with open(f'./server_folder/{file_name}', 'wb') as f:
                f.write(decrypted_data)

        print("File received and decrypted successfully")
        


    elif choice == '2': # Check Sums
        print('The client has chosen to do a integrity verification (checksums)... now checking integrity.')

        #Receiving the check sum size and the file size 
        data = client.recv(4 + file_size)

        received_checksum = int.from_bytes(data[:4], byteorder='big')
        file_data = data[4:]

        calculated_checksum = calculate_crc32(file_data)

        if received_checksum == calculated_checksum:
            with open(f'./server_folder/{file_name}', 'wb') as f:
                f.write(file_data)
            print("File received, and checksum verified successfully")
        else:
            print("Checksum verification failed. Data may be corrupted.")
        

    else: # Choice == '3' is the default (Both)
        print('The client has chosen to do both checksums and encryption... now checking sums and decrypting.')

        key = derive_key(password, salt)
        with client:
            #Receive the check sum size, IV, and the file size
            data = client.recv(4 + 16 + file_size)
            #The first 4 bytes are the check sum
            received_checksum = int.from_bytes(data[:4], byteorder='big')
            #The bytes from 4-20 contain the IV
            iv = data[4:20]
            #Everything after 20 bytes is the encrypted data
            encrypted_data = data[20:]
            decrypted_data = decrypt_file(encrypted_data, key, iv)

            calculated_checksum = calculate_crc32(data[4:])

            print(f'The sums are: \n calculated checksum: {calculated_checksum} \n received cheksum: {received_checksum}' )
            print(calculated_checksum)
            print(received_checksum)

        if received_checksum == calculated_checksum:
            with open(f'./server_folder/{file_name}', 'wb') as f:
                f.write(decrypted_data)
            print("File received, and checksum verified successfully")
        else:
            print("Checksum verification failed. Data may be corrupted.")

            
    client.close()


if __name__ == '__main__':
    server.listen()
    print(f"[ACTIVE] the server is now listening on {IP}: {PORT}...")
    client, address = server.accept()
    print(f'A connection from {str(address)} has started')
    start(client)
    