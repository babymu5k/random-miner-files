print("version 1.5.0")
print("made by superpythonguy")
print("could have bugs")

import hashlib
import os
from socket import socket
import sys
import time
import ssl
import select
from json import load as jsonload
import requests
import random
soc = socket()
time.sleep(1)
greetings = ("Hello and thanks for using me Experimental duinocoin miner", "DUINOCOINSSS!!", "DuinoCoin made is a coin made by Revox and many others")
rg = random.choice(greetings)
print(rg)
print("structure from minimal pc miner")
time.sleep(1)
print("this could be glithcy made for FUN ")
def current_time():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time
dusr = input("what is you duinocoin username\n>>>")   # asks for duino username
diff_choice = input("do you want to use low or normal difficulty(low for old PCs and rasp) yes or no\n>>>") # asks for difficulty
if diff_choice == "yes":
    print("you chonsen yes")
    useldiff = True
else:
    print("you have chosen no")
    useldiff = False

def get_pools():
    while True:
        try:
            res = requests.get(
                "https://server.duinocoin.com/getPool"
                ).json()

            duinoip = res["ip"]
            port = res["port"]

            return duinoip, port
        except Exception as e:
            print (f'{current_time()} : Error retrieving mining node, retrying in 3s') # if it fails
            time.sleep(3)

while True:                                        # loop
    try:
        print(f"{current_time()} : finding quickest connection to the Duinocoin servers")
        print("...waiting...")
        try:
            duinoip, port = get_pools()
        except Exception as e:
            duinoip = "server.duinocoin.com"
            port = 2813
            print(f'{current_time()} : getting Duinos default server port and address get ready to mine :)')

        soc.connect((str(duinoip), int(port)))
        print(f"{current_time()} : Stable connection has been found")
        print("almost ready to mine")
        server_version = soc.recv(100).decode()
        print("server version is", server_version)

        while True:
            if useldiff:
                soc.send(bytes(
                    "JOB,"
                    + str(dusr)
                    + ",MEDIUM",
                    encoding="utf8"))

            else:
                soc.send(bytes(
                    "JOB,"
                    + str(dusr),
                    encoding="utf8"))

            job = soc.recv(1024).decode().rstrip("\n")

            job = job.split(",")
            difficulty = job[2]

            hashingStartTime = time.time()
            base_hash = hashlib.sha1(str(job[0]).encode('ascii'))
            temp_hash = None

            for result in range(1000 * int(difficulty) + 1):
                temp_hash = base_hash.copy()
                temp_hash.update(str(result).encode('ascii'))
                ducos1 = temp_hash.hexdigest()

                if job[1] == ducos1:
                    hashingStopTime = time.time()
                    timeDifference = hashingStopTime - hashingStartTime
                    hashrate = result / timeDifference

                    soc.send(bytes(
                        str(result)
                        + ","
                        + str(hashrate)
                        + ",[python miner]",
                        encoding="utf8"))

                    feedback = soc.recv(1024).decode().rstrip("\n")
                    if feedback == "GOOD":
                        print(f'{current_time()} : share is accepted',
                            result,
                            "Hashrate",
                            int(hashrate / 1000),
                            "kH/s (unit used to measure hash per second)",
                            "Difficulty is",
                            difficulty)
                        break

                    elif feedback == "BAD":
                        print(f'{current_time()} : share is Rejected',
                            result,
                            "Hashrate",
                            int(hashrate / 1000),
                            "kH/s",
                            "Difficulty is",
                            difficulty)
                        break

    except Exception as e:
        print(f'{current_time()} : Error occured: ' + str(e) + ", restarting in 3s.")
        time.sleep(3)
        os.execl(sys.executable, sys.executable, *sys.argv)