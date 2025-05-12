
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
import time
import Sensor

import random

currentMode='boot'
lastMode=''
battery=100
solar_check=False
downlink_error=0

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
    print(f"'{input_file}' encrypted and sent as '{output_file}', then deleted.")

def boot():
    global currentMode
    print("Deploying solar panels", end="")
    for _ in range(3):
        time.sleep(1)
        print(".", end="", flush=True)
    print("\n")
    print("Solar panels deployed!")
    time.sleep(1)
    print("Deploying subsystems", end="")
    for _ in range(3):
        time.sleep(1)
        print(".", end="", flush=True)
    print("\n")
    print("Deployment complete entering standby mode!")
    currentMode='standby'
    return
    

def standby():
    print("Standby awaiting instructions", end="")
    for _ in range(3):
        time.sleep(1)
        print(".", end="", flush=True)
    print("\n")
    global solar_check
    global currentMode
    global lastMode
    global battery
    lastMode=currentMode
    if (battery<=20):
        print("low battery entering safe mode to conserve power\n")
        currentMode='safe'
        return
    elif solar_check:
        print("On day light side, preparing to gather data!\n")
        currentMode = 'nominal'
    else:
        time.sleep(5)
        solar_check=True
        battery = battery - random.randint(1,3)
    return

def nominal():
    global currentMode
    global solar_check
    global battery
    if (battery<=20):
        print("low battery entering safe mode to conserve power\n")
        currentMode='safe'
        return
    else:
        print("gathering pressure daata")
        Sensor.simulate_pressure_sensor()
        print("gathering particle data")
        Sensor.simulate_optical_particle_sensor()
        print("gathering spectroscopic data")
        Sensor.simulate_spectrometer_sensor()
        currentMode='downlink'
        solar_check=False
        battery = battery - random.randint(1,10)
        return


def downlink():
    # Usage
    global currentMode
    global battery
    global downlink_error
    if (battery<=20):
        print("low battery entering safe mode to conserve power\n")
        currentMode='safe'
        return
    elif (downlink_error>=3):
        print("To many downlink errors, entering safe mode to troubleshoot")
        currentMode='safe'
        return
    elif(random.randint(1,2)==1):
        print("Downlink error, trying again...")
        downlink_error = downlink_error + 1
        battery = battery - random.randint(1,5)
        return
    else:
        print("Sending encrypted data to Ground Station!!!")
        CommsWithGS('preassure_data.csv', 'preassure_data.aes', 'RackarnsRabarber')
        CommsWithGS('orbital_sensor_data.csv', 'orbital_sensor_data.aes', 'RackarnsRabarber')
        CommsWithGS('spectrometer_data.csv', 'spectrometer_data.aes', 'RackarnsRabarber')
        downlink_error=0
        currentMode='standby'
        battery = battery - random.randint(1,10)
        return


def safe():
    global battery
    global currentMode
    global lastMode
    global downlink_error
    print("safe mode")
    if battery<=20:
        print("Recharging battery please stand by...")
        for i in range(battery,100):
            battery+=1
            print(f"Battery at {battery}%, charging...")
            time.sleep(0.1)
        print(f"battery now recharged returning to {lastMode} mode")
        currentMode = lastMode
        return
    elif(downlink_error>=3):
        print("Telecommunication error")
        print("Rebooting Telecomunication subsystem", end="")
        for _ in range(3):
            time.sleep(1)
            print(".", end="", flush=True)
        downlink_error=0
        print("\n")
    else:
        print("The error has been handled, returning to standby mode")
        currentMode='standby'
        return
        
            


def modeChange(mode):
    #change the modes i.e. safe mmode, boot mode etc.
    match mode:
            case 'boot':
                print(f"entering {mode} mode\n")
                boot()
            case 'standby':
                standby()
            case 'nominal':
                print(f"entering {mode} mode\n")
                nominal()
            case 'downlink':
                print(f"entering {mode} mode\n")
                downlink()
            case 'safe':
                print(f"entering {mode} mode\n")
                safe()
            case _:
                print(f"Unknown mode: '{mode}' entering safe mode instead")
                modeChange('safe')
    return
            
def main():
    while(True):
        modeChange(currentMode)
        print(currentMode)
        print("\n")
        time.sleep(2)


if (__name__ == "__main__"):
    main()

