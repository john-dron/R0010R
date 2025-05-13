#This is the main file for the ground station
from Crypto.Cipher import AES
import hashlib
import os
import time
import re

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def generate_key(passphrase: str) -> bytes:
    return hashlib.sha256(passphrase.encode()).digest()[:16]

def decrypt_file(encrypted_file: str, output_file: str, passphrase: str):
    with open(encrypted_file, 'rb') as f:
        file_data = f.read()

    iv = file_data[:16]
    encrypted_data = file_data[16:]
    key = generate_key(passphrase)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data))

    with open(output_file, 'ab') as f:
        f.write(decrypted_data)

    print(f"'{encrypted_file}' recieved! It's decypted and saved as '{output_file}'.")

# Usage
def main():
    pattern = re.compile(r'^.*\.aes$')
    waiting_message_shown = False
    while(True):
        aes_files = [f for f in os.listdir('.') if pattern.match(f)]

        if aes_files:
            if waiting_message_shown:
                print()  # End the "waiting" line cleanly
                waiting_message_shown = False
            
            for filename in aes_files:
                output_file = filename.replace('.aes', '_recieved.csv')
                decrypt_file(filename, output_file, 'RackarnsRabarber')
                os.remove(filename)
        else:
            for i in range(4):  # Show up to 3 dots
                dots = '.' * i
                message = f"\rNo current uplink. Waiting{dots:<3}"  # Pad to overwrite previous
                print(message, end='', flush=True)
                time.sleep(1)
            time.sleep(1)  # Slight pause before retrying
            waiting_message_shown = True
            



if (__name__ == "__main__"):
    main()
