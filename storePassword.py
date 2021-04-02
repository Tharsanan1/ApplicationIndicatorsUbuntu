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


hashed_password_path = join(dirname(__file__), '.hashed_password')

password_usr = getpwd()
print("password : " + password)

hashed_input_password = hashlib.sha512(password.encode('utf-8')).hexdigest()



with open(hashed_password_path, 'w') as output_file:
    output_file.write(hashed_input_password)
