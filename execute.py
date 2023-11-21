#############
# Libraries #
#############

from cryptography.fernet import Fernet
import time
import hmac
import sys

#############
# Functions #
#############

def store_key(key):
    try:
        with open(sys.argv[1], "rb") as f:
            key = f.read()
    except:
        print("Error: (open) " + sys.argv[1] + " couldn't be opened")
        return
    try:
        hex_key = int(key, 16)
        hex_key = str(key)
        if len(hex_key) < 64:
            print("./ft_otp: error: key must be 64 hexadecimal characters.")
            return
        key = Fernet.generate_key()
        with open("./.key", "wb") as f:
            f.write(key)
        key = Fernet(key)
        with open("./ft_otp.key", "wb") as f:
            f.write(key.encrypt(hex_key.encode()))
            print("Key was successfully saved in ft_otp.key.")
    except:
        print("./ft_otp: error: key must be 64 hexadecimal characters.")
        return

def create_key(master_key):
    try:
        with open(".key", "rb") as f:
            key = f.read()
        key = Fernet(key)
        with open(master_key, "rb") as f:
            master_key = f.read()
        master_key = key.decrypt(master_key)
    except:
        print("Error: (open) can't obtain master key")
        return
    counter = str(time.time() // 30)
    hmac_sha1 = hmac.new(master_key, counter.encode(), "sha1")
    hmac_sha1 = hmac_sha1.hexdigest()
    offset = int(hmac_sha1[39], 16)
    totp = hmac_sha1[offset*2:offset*2 + 8]
    totp = str(int(totp[0], 16) & 0x7) + totp[1:]
    totp = int(totp, 16)
    totp = str(totp%(10**6))
    while len(totp) != 6:
        totp += "0"
    print(totp)

##################################
# Program: python execute.py S G #
##################################

if sys.argv[1] != "0" and sys.argv[2] != "0":
    print("Error: (format) ./program [-gk]")
    exit(1)

if sys.argv[1] != "0":
    store_key(sys.argv[1])
elif sys.argv[2] != "0":
    create_key(sys.argv[2])
