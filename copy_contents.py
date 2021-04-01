# This code is an example for a tutorial on Ubuntu Unity/Gnome AppIndicators:
# http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html

import os
import signal
import json
import pyperclip

import hmac, base64, struct, hashlib, time

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from os.path import join, dirname
from dotenv import load_dotenv
 
# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')
print("path : " + dotenv_path)
# Load file from the path.
load_dotenv(dotenv_path)

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
    password = "95L?f=6Fm3n-"
    return "Copied " + password

def copy_trace_pass(_):
    notify.Notification.new("Success", copy_trace_pass_impl(), None).show()



def copy_totp_dev_impl():
    password = os.getenv('DEV_PASSWORD') + str(get_totp_token(os.getenv('TOTP_DEV_SECRET'))).zfill(6)
    return "Copied " + password

def copy_totp_dev(_):
    notify.Notification.new("Success", copy_totp_dev_impl(), None).show()



def copy_totp_gateway_impl():
    password = os.getenv('PAYMENT_PASSWORD') + str(get_totp_token(os.getenv('TOTP_PAYMENT_SECRET'))).zfill(6)
    return "Copied " + password

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
