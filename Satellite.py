
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
import time
import Sensor
import random
import re
from datetime import datetime

#Set initial values for the satellite, i.e. boot mode, no previous mode, 100% battery, no solar light and no downlink errors
currentMode='boot'
lastMode=''
battery=40
solar_check=False
downlink_error=0

def pad(data):
    #Set the amount of padding needed as AES-128 uses 16 byte chunks
    pad_len = 16 - len(data) % 16
    return data + bytes([pad_len]) * pad_len

def generate_key(passphrase: str) -> bytes:
    #use a preexisting library to generate the AES-128 key
    return hashlib.sha256(passphrase.encode()).digest()[:16]

def CommsWithGS(input_file: str, output_file: str, passphrase: str):
    #Start reading the data file that will get transfered
    with open(input_file, 'rb') as f:
        data = f.read()

    #Generate a Hash key based on the passphrase used
    key = generate_key(passphrase)
    #Generate a random Initialization Vector for security
    iv = get_random_bytes(16)
    #Generate the cipher using the Key and the IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    #Encrypts using said cipher
    encrypted_data = cipher.encrypt(pad(data))

    #Creates the file nessecary for communication
    with open(output_file, 'wb') as f:
        f.write(iv + encrypted_data)

    moved='backup/' + input_file
    os.rename(input_file, moved)
    print(f"'{input_file}' encrypted and sent as '{output_file}' and moved the original to '{moved}'")

def boot():
    global currentMode
    #Pretend solar panels get deployed
    print("Deploying solar panels", end="")
    #Generate ellipsis at end of waiting message
    for _ in range(3):
        time.sleep(1)
        print(".", end="", flush=True)
    print("\n")
    print("Solar panels deployed!")
    time.sleep(1)
    #Same as for solar panels
    print("Deploying subsystems", end="")
    for _ in range(3):
        time.sleep(1)
        print(".", end="", flush=True)
    print("\n")
    print("Deployment complete entering standby mode!")
    #Set mode to standby so that it will enter standby after this
    currentMode='standby'
    return
    

def standby():
    #Print satement for waiting
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
    #Checks if there is low battery on the satellite, if low battery enter safe mode
    if (battery<=20):
        print("low battery entering safe mode to conserve power\n")
        currentMode='safe'
        return
    #If we are on the day side, idicated by sunlight we enter nominal mode to collect data
    elif solar_check:
        print("On day light side, preparing to gather data!\n")
        currentMode = 'nominal'
    #If we are not on the day side, wait until we are, and set that to be true
    else:
        time.sleep(5)
        solar_check=True
        #Arbitrary battery drain, this is python code it won't drain otherwise
        battery = battery - random.randint(1,3)
    return

def nominal():
    global currentMode
    global solar_check
    global battery
    #Chech if enough battery
    if (battery<=20):
        print("low battery entering safe mode to conserve power\n")
        currentMode='safe'
        #If low battery day scan missed set to night
        solar_check=False
        return
    #Enough power means we get data
    else:
        #Get all data from Sensor.py
        print("gathering pressure daata")
        Sensor.simulate_pressure_sensor()
        print("gathering particle data")
        Sensor.simulate_optical_particle_sensor()
        print("gathering spectroscopic data")
        Sensor.simulate_spectrometer_sensor()
        #Set mode to downlink
        currentMode='downlink'
        #Set to night side of the earth
        solar_check=False
        #Arbitrary battery drain
        battery = battery - random.randint(1,10)
        return


def downlink():
    # Usage
    global currentMode
    global battery
    global downlink_error
    #Get the timestamp so as to not overwrite encrypted files if the GS cant collect them
    #time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    #Check battery
    if (battery<=20):
        print("low battery entering safe mode to conserve power\n")
        currentMode='safe'
        return
    #If there are to many downlink fails in a row enter safe mode to handle why
    elif (downlink_error>=3):
        print("To many downlink errors, entering safe mode to troubleshoot")
        currentMode='safe'
        return
    #Arbitrary downlink fail, 50% chance of it happening
    elif(random.randint(1,2)==1):
        print("Downlink error, trying again...")
        #If failed add one to the counter
        downlink_error = downlink_error + 1
        #Arbitrary battery drain, though smaller as it wasn't that successfull
        battery = battery - random.randint(1,5)
        return
    #Successfull communication engcrypt all the .csv data files using time stamp so as to not overwrite any thing
    else:
        print("Sending encrypted data to Ground Station!!!")
        pattern = re.compile(r'^.*\.csv$')
        csv_files = [f for f in os.listdir('.') if pattern.match(f)]
        #If there are files decrypt them
        if csv_files:
            #Decrypt all .aes files found
            for filename in csv_files:
                output_file = filename.replace('.csv', '.aes')
                CommsWithGS(filename, output_file, 'RackarnsRabarber')
        #Set error to 0 as new cycle beggins
        downlink_error=0
        currentMode='standby'
        #Arbitrary battery drain
        battery = battery - random.randint(1,10)
        return


def safe():
    global battery
    global currentMode
    global lastMode
    global downlink_error
    print("safe mode")
    #If low battery, charge it to 100 and enter last mode it had
    if battery<=20:
        print("Recharging battery please stand by...")
        #Arbetrary charging
        for i in range(battery,100):
            battery+=1
            print(f"\rBattery at {battery}%, charging...", end='', flush=True)
            time.sleep(0.2)
        print(end='\n')
        print(f"battery now recharged returning to {lastMode} mode")
        currentMode = lastMode
        return
    #If downlink error arbitrary reboot of telecommunication, though this is just text
    elif(downlink_error>=3):
        print("Telecommunication error")
        print("Rebooting Telecomunication subsystem", end="")
        for _ in range(3):
            time.sleep(1)
            print(".", end="", flush=True)
        downlink_error=0
        print("\n")
        currentMode='standby'
        return
    #Else it is handled and set to standby mode, no specific error should end up here
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
            #If somehow it gets input data of a mode that is undefinied enter safe mode instead
            case _:
                print(f"Unknown mode: '{mode}' entering safe mode instead")
                modeChange('safe')
    return
            
def main():
    #Continous loop of modes, sleep 2 between mode for readability in output
    while(True):
        modeChange(currentMode)
        print(currentMode)
        print("\n")
        time.sleep(2)


if (__name__ == "__main__"):
    main()

