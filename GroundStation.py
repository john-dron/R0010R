#This is the main file for the ground station
from Crypto.Cipher import AES
import hashlib

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

    with open(output_file, 'wb') as f:
        f.write(decrypted_data)

    print(f"'{encrypted_file}' decrypted and saved as '{output_file}'.")

# Usage
decrypt_file('coms.aes', 'data_decrypted.csv', 'RackarnsRabarber')

#def readComms():
    #define how to read from the comms file
#    print("test")


#new test 3