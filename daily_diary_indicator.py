
import os
import signal
import json
import pyperclip
import subprocess
from datetime import datetime
import hmac, base64, struct, hashlib, time

import webbrowser
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

from os.path import join, dirname

APPINDICATOR_ID = 'startdiaryindicator'

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('/home/tharsanan/Projects/AppIndicatorsUbuntu/diary.png'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu = gtk.Menu()

    item_open_today_note = gtk.MenuItem('Open Today Note')
    item_open_today_note.connect('activate', open_today_note)
    menu.append(item_open_today_note)
    list_of_files = os.listdir(join(dirname(__file__), 'notes'))
    list_of_files.sort(reverse=True)
    print(list_of_files)
    for filename in list_of_files[1:10]:
        print(filename)
        if filename.endswith(".note"): 
            item_note = gtk.MenuItem(filename)
            item_note.connect('activate', open_note)
            menu.append(item_note)
            continue
        else:
            continue

    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)

    menu.show_all()
    return menu

def open_note(_):
    print(_.get_label())
    note_path = join(dirname(__file__), 'notes/' , _.get_label())
    webbrowser.open(note_path)

def open_today_note(_):
    today_note_path = join(dirname(__file__), 'notes/' , (datetime.today().strftime('%Y-%m-%d')+".note"))
    if not os.path.exists(today_note_path):
        with open(today_note_path, "w+"):
            pass
    webbrowser.open(today_note_path)

def quit(_):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
