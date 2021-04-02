import os
import signal
import json
import pyperclip
import hashlib, uuid
import hmac, base64, struct, hashlib, time
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from os.path import join, dirname
from dotenv import load_dotenv
from tkinter import *


def decrypt(key, source, decode=True):
    if decode:
        source = base64.b64decode(source.encode("latin-1"))
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return data[:-padding]  # remove the padding

password = ''

def getpwd():
    global password
    root = Tk()
    pwdbox = Entry(root, show = '*')
    pwdbox.focus_set()
    def onpwdentry(evt):
        global password
        password = pwdbox.get()
        print ("entry : " + password)
        root.destroy()
    def onokclick():
        global password
        password = pwdbox.get()
        print ("Click : " + password)
        root.destroy()
    Label(root, text = 'Password').pack(side = 'top')

    pwdbox.pack(side = 'top')
    pwdbox.bind('<Return>', onpwdentry)
    Button(root, command=onokclick, text = 'OK').pack(side = 'top')

    root.mainloop()
    return password


def showError(msg):
    root = Tk()
    Label(root, text = msg).pack(side = 'top')
    def onokclick():
        root.destroy()
    Button(root, command=onokclick, text = 'OK').pack(side = 'top')
    root.mainloop()
    return


hashed_password_path = join(dirname(__file__), '.hashed_password')
with open(hashed_password_path, 'r') as file:
    global hashed_password_data
    hashed_password_data = file.read().replace('\n', '')

print (hashed_password_data)
password_usr = getpwd()
print("password : " + password)

hashed_input_password = hashlib.sha512(password.encode('utf-8')).hexdigest()

if (hashed_input_password != hashed_password_data):
    showError("Password is wrong")
    sys.exit()




dotenv_path = join(dirname(__file__), '.env')

with open(dotenv_path, 'r') as file:
    global encrypted_data
    encrypted_data = file.read()

global dotenv_decrypted_data
dotenv_decrypted_data = decrypt(password.encode('utf-8'), encrypted_data).decode('utf-8')

with open(dotenv_path, 'w') as output_file:
    output_file.write(dotenv_decrypted_data)
