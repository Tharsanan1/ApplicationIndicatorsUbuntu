
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


APPINDICATOR_ID = 'startappsindicator'

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('/home/tharsanan/Projects/AppIndicatorsUbuntu/app.png'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu = gtk.Menu()

    item_start_google = gtk.MenuItem('Google')
    item_start_google.connect('activate', start_google)
    menu.append(item_start_google)

    item_start_postman = gtk.MenuItem('Postman')
    item_start_postman.connect('activate', start_postman)
    menu.append(item_start_postman)

    item_start_eclipse = gtk.MenuItem('Eclipse')
    item_start_eclipse.connect('activate', start_eclipse)
    menu.append(item_start_eclipse)

    item_start_solr = gtk.MenuItem('Solr')
    item_start_solr.connect('activate', start_solr)
    menu.append(item_start_solr)

    
    
    # item_open_configs_folder = gtk.MenuItem('Open Configs folder')
    # item_open_configs_folder.connect('activate', open_configs_folder)
    # menu.append(item_open_configs_folder)

    # item_open_projects_folder = gtk.MenuItem('Open Projects folder')
    # item_open_projects_folder.connect('activate', open_projects_folder)
    # menu.append(item_open_projects_folder)

    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)

    menu.show_all()
    return menu


def start_google(_):
    subprocess.call("google-chrome &", shell=True)

def start_solr(_):
    subprocess.call("/home/tharsanan/Software/solr-8.6.1/bin/solr start &", shell=True)

def start_postman(_):
    subprocess.call("/home/tharsanan/Software/Postman-linux-x64-7.24.0/Postman/Postman &", shell=True)

def start_eclipse(_):
    subprocess.call("/home/tharsanan/eclipse/jee-2019-03/eclipse/eclipse &", shell=True)

# def open_configs_folder(_):
#     subprocess.call("nautilus /home/tharsanan/EnactorHome/configs/web_shop_2_6", shell=True)

# def open_projects_folder(_):
#     subprocess.call("nautilus /home/tharsanan/Projects", shell=True)

def quit(_):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
