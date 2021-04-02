# This code is an example for a tutorial on Ubuntu Unity/Gnome AppIndicators:
# http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html

import os
import signal
import json
import pyperclip
import hashlib, uuid
import hmac, base64, struct, hashlib, time
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from os.path import join, dirname
from dotenv import load_dotenv
from tkinter import *

password = ''

def getpwd():
    global password
    root = Tk()
    root.eval('tk::PlaceWindow . center')
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
    root.eval('tk::PlaceWindow . center')
    Label(root, text = msg).pack(side = 'top')
    def onokclick():
        root.destroy()
    def returnClick(args):
        root.destroy()
    btn  = Button(root, command=onokclick, text = 'OK').pack(side = 'top')
    root.bind("<Return>", returnClick)
    root.mainloop()
    return

def encrypt(key, source, encode=True):
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    return base64.b64encode(data).decode("latin-1") if encode else data

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
    global dotenv_encrypted_data
    dotenv_encrypted_data = file.read()

global dotenv_decrypted_data
dotenv_decrypted_data = decrypt(password.encode('utf-8'), dotenv_encrypted_data).decode('utf-8')

with open(dotenv_path, 'w') as output_file:
    output_file.write(dotenv_decrypted_data)


print("path : " + dotenv_path)
print (dotenv_decrypted_data)
load_dotenv(dotenv_path)


with open(dotenv_path, 'w') as output_file:
    dotenv_re_encrypted_data = encrypt(password.encode('utf-8'), dotenv_decrypted_data.encode('utf-8'))
    output_file.write(dotenv_re_encrypted_data)

APPINDICATOR_ID = 'copycontentsindicator'

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('/home/tharsanan/Projects/AppIndicatorsUbuntu/copy.png'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu = gtk.Menu()

    item_copy_trace_pass = gtk.MenuItem('Copy trace pass')
    item_copy_trace_pass.connect('activate', copy_trace_pass)
    menu.append(item_copy_trace_pass)

    item_copy_totp_dev = gtk.MenuItem('Copy TOTP DEV')
    item_copy_totp_dev.connect('activate', copy_totp_dev)
    menu.append(item_copy_totp_dev)

    item_copy_totp_gateway = gtk.MenuItem('Copy TOTP GATEWAY')
    item_copy_totp_gateway.connect('activate', copy_totp_gateway)
    menu.append(item_copy_totp_gateway)

    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)

    menu.show_all()
    return menu

def copy_trace_pass_impl():
    password = os.getenv('TRACE_SERVER_PASSWORD')
    pyperclip.copy(password)
    return "Copied " 

def copy_trace_pass(_):
    info = notify.Notification.new("Success", copy_trace_pass_impl(), None)
    info.set_timeout(500)
    info.set_urgency(1)
    info.show()



def copy_totp_dev_impl():
    password = os.getenv('DEV_PASSWORD') + str(get_totp_token(os.getenv('TOTP_DEV_SECRET'))).zfill(6)
    pyperclip.copy(password)
    return "Copied. time left " + str(30 - int(time.time())%30) + "s" 

def copy_totp_dev(_):
    notify.Notification.new("Success", copy_totp_dev_impl(), None).show()



def copy_totp_gateway_impl():
    password = os.getenv('PAYMENT_PASSWORD') + str(get_totp_token(os.getenv('TOTP_PAYMENT_SECRET'))).zfill(6)
    pyperclip.copy(password)
    return "Copied. time left " + str(30 - int(time.time())%30) + "s" 

def copy_totp_gateway(_):
    notify.Notification.new("Success", copy_totp_gateway_impl(), None).show()


def quit(_):
    notify.uninit()
    gtk.main_quit()

def get_hotp_token(secret, intervals_no):
    
    if(len(secret)%8 != 0) :
        key = base64.b32decode(secret + '========'[:((((len(secret)//8) + 1) * 8) - len(secret))], True)
    else:
        key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return h

def get_totp_token(secret):
    return get_hotp_token(secret, intervals_no=int(time.time())//30)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
