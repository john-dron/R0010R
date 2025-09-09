#This is the main file for the ground station
from Crypto.Cipher import AES
import hashlib
import os
import time
import re

def unpad(data):
    #Checks the amount of padding used in the specific file
    pad_len = data[-1]
    return data[:-pad_len]

def generate_key(passphrase: str) -> bytes:
    return hashlib.sha256(passphrase.encode()).digest()[:16]

def decrypt_file(encrypted_file: str, output_file: str, passphrase: str):
    #Read the ecryptd file
    with open(encrypted_file, 'rb') as f:
        file_data = f.read()

    #Takes the first 16 bytes from the encrypted file to use for correct derypt
    iv = file_data[:16]
    #The actual encrypted contents of the file
    encrypted_data = file_data[16:]
    #Generate the AES key to decrypt the file
    key = generate_key(passphrase)
    #Generate the cipher used to decrypt using the key
    cipher = AES.new(key, AES.MODE_CBC, iv)
    #Removes the AES padding
    decrypted_data = unpad(cipher.decrypt(encrypted_data))

    #Append to the output file, if it exists this creates it
    with open(output_file, 'ab') as f:
        f.write(decrypted_data)

    print(f"'{encrypted_file}' recieved! It's decypted and saved as '{output_file}'.")

# Usage
def main():
    #Set a reggex pattern to search for any .aes files i.e. any encrypted files
    pattern = re.compile(r'^.*\.aes$')
    #For a clean line break after the waiting line
    waiting_message_shown = False
    #Start a Loop waiting for files to decrypt, the communication
    while(True):
        #Chech through the directory for any .aes files
        aes_files = [f for f in os.listdir('.') if pattern.match(f)]
        #If there are files decrypt them
        if aes_files:
            if waiting_message_shown:
                print()  # End the "waiting" line cleanly
                waiting_message_shown = False
            #Decrypt all .aes files found
            for filename in aes_files:
                output_file = 'gs/' + filename.replace('.aes', '_recieved.csv')
                #output_file = 'gs/' + output_file
                decrypt_file(filename, output_file, 'RackarnsRabarber')
                #Remove the encrypted version of the file to save storage
                os.remove(filename)
        else:
            #Loop the waiting message with ellipsis
            for i in range(4):  # Show up to 3 dots
                dots = '.' * i
                message = f"\rNo current uplink. Waiting{dots:<3}"  # Pad to overwrite previous
                print(message, end='', flush=True)
                time.sleep(1)
            time.sleep(1)  # Slight pause before retrying
            waiting_message_shown = True
            

if (__name__ == "__main__"):
    #Makes sure main runs if this file is started by it self
    main()
