
import os
import signal
import json
import pyperclip
import subprocess

import hmac, base64, struct, hashlib, time

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

from os.path import join, dirname


APPINDICATOR_ID = 'openfolderindicator'

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('/home/tharsanan/Projects/AppIndicatorsUbuntu/fileexp.png'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu = gtk.Menu()

    item_open_payment_folder = gtk.MenuItem('Open Payment folder')
    item_open_payment_folder.connect('activate', open_payment_folder)
    menu.append(item_open_payment_folder)

    item_open_enactor_home_folder = gtk.MenuItem('Open EnactorHome folder')
    item_open_enactor_home_folder.connect('activate', open_enactor_home_folder)
    menu.append(item_open_enactor_home_folder)

    item_open_logs_folder = gtk.MenuItem('Open Logs folder')
    item_open_logs_folder.connect('activate', open_logs_folder)
    menu.append(item_open_logs_folder)

    item_open_postman_folder = gtk.MenuItem('Open Postman folder')
    item_open_postman_folder.connect('activate', open_postman_folder)
    menu.append(item_open_postman_folder)
    
    item_open_configs_folder = gtk.MenuItem('Open Configs folder')
    item_open_configs_folder.connect('activate', open_configs_folder)
    menu.append(item_open_configs_folder)

    item_open_projects_folder = gtk.MenuItem('Open Projects folder')
    item_open_projects_folder.connect('activate', open_projects_folder)
    menu.append(item_open_projects_folder)

    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)

    menu.show_all()
    return menu


def open_payment_folder(_):
    subprocess.call("nautilus /home/tharsanan/payment", shell=True)

def open_enactor_home_folder(_):
    subprocess.call("nautilus /home/tharsanan/EnactorHome", shell=True)

def open_logs_folder(_):
    subprocess.call("nautilus /home/tharsanan/EnactorHome/WebShop_2_6/Logs", shell=True)

def open_postman_folder(_):
    subprocess.call("nautilus /home/tharsanan/Software/Postman-linux-x64-7.24.0/Postman", shell=True)

def open_configs_folder(_):
    subprocess.call("nautilus /home/tharsanan/EnactorHome/configs/web_shop_2_6", shell=True)

def open_projects_folder(_):
    subprocess.call("nautilus /home/tharsanan/Projects", shell=True)

def quit(_):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
