
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
from Sensor import generate_and_save_numbers

def pad(data):
    pad_len = 16 - len(data) % 16
    return data + bytes([pad_len]) * pad_len

def generate_key(passphrase: str) -> bytes:
    return hashlib.sha256(passphrase.encode()).digest()[:16]  # AES-128 key

def CommsWithGS(input_file: str, output_file: str, passphrase: str):
    with open(input_file, 'rb') as f:
        data = f.read()

    key = generate_key(passphrase)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data))

    with open(output_file, 'wb') as f:
        f.write(iv + encrypted_data)

    os.remove(input_file)
    print(f"'{input_file}' encrypted and saved as '{output_file}', then deleted.")


def main():
    for i in range(5) :
        generate_and_save_numbers(500)

    # Usage
    CommsWithGS('data.csv', 'coms.aes', 'RackarnsRabarber')    
    
if (__name__ == "__main__"):
    main()

#def modeChange():
    #change the modes i.e. afe mmode, boot mode etc.
#    print("temp")