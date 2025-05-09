
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
import time
import Sensor
#from Sensor import generate_and_save_numbers
#from particlesens import simulate_optical_particle_sensor
#from Spectrometer import simulate_spectrometer_sensor
import random

currentMode='boot'
lastMode=''
battery=100
solar_check=False

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
    print("deploying solar panel\n")
    global currentMode
    global battery
    global lastMode
    lastMode=currentMode
    time.sleep(1)
    print("cheching battery power\n")
    if(battery<=20):
        print("low battery entering safe mode to conserve power\n")
        currentMode='safe'
        return
    else:
        print("deployment complete entering standby mode!\n")
        currentMode='standby'
        return
    

def standby():
    print("standby awaiting instructions\n")
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
        print("gathering senosordata 1")
        Sensor.generate_and_save_numbers()
        print("gathering particle data")
        Sensor.simulate_optical_particle_sensor()
        print("gathering spectroscopic data\n")
        Sensor.simulate_spectrometer_sensor()
        currentMode='downlink'
        solar_check=False
        battery = battery - random.randint(1,10)
        return


def downlink():
    # Usage
    global currentMode
    global battery
    if (battery<=20):
        print("low battery entering safe mode to conserve power\n")
        currentMode='safe'
        return
    else:
        print("Sending encrypted data to Ground Station!!!")
        CommsWithGS('preassure_data.csv', 'preassure_data.aes', 'RackarnsRabarber')
        CommsWithGS('orbital_sensor_data.csv', 'orbital_sensor_data.aes', 'RackarnsRabarber')
        CommsWithGS('spectrometer_data.csv', 'spectrometer_data.aes', 'RackarnsRabarber')
        currentMode='standby'
        battery = battery - random.randint(1,10)
        return


def safe():
    global battery
    global currentMode
    global lastMode
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
    else:
        currentMode='standby'
        return
        
            


def modeChange(mode):
    #change the modes i.e. safe mmode, boot mode etc.
    match mode:
            case 'boot':
                print(f"entering {mode} mode\n")
                boot()
            case 'standby':
                print(f"entering {mode} mode\n")
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

