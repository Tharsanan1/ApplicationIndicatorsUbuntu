
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
import time
import threading


APPINDICATOR_ID = 'movementindicator'

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('/home/tharsanan/Projects/AppIndicatorsUbuntu/movement.png'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()
global t1
stopThread = False

def build_menu():
    menu = gtk.Menu()
    # global t1
    # t1 = threading.Thread(target=movementReminderProcessor)
    # t1.start()
    # item_quit = gtk.MenuItem('Quit')
    # item_quit.connect('activate', quit)
    # menu.append(item_quit)

    item_quit1 = gtk.CheckMenuItem('Quit')
    # item_quit1.connect('activate', quit)
    menu.append(item_quit1)

    menu.show_all()
    return menu



def movementReminderProcessor():
    skippedCount = 0
    while (True) :
        global stopThread
        if(stopThread) :
            break
        time.sleep(60 * 20)
        result = showReminder(skippedCount)
        if (result != "OKEYED"):
            print("if")
            skippedCount = skippedCount +  1
        
        
        print(result + " " + str(skippedCount))
 
def showReminder(skippedCount):
    root = Tk()
    root.eval('tk::PlaceWindow . center')
    global result
    result = ""

    def onOkClick():
        global result
        result = "OKEYED"
        print ("result " + result)
        root.destroy()
    def onSkipClick():
        global result
        result = "SKIPPED"
        root.destroy()
    
    labelTxt = 'Dont just sit there. Move! Move!'

    if (skippedCount >= 3) :
        labelTxt = 'Yo man you are skipping it for ' + str(skippedCount) + " times. Standup, go get some water and drink. This is the final warning."

    Label(root, text = labelTxt).pack(side = 'top')

    Button(root, command=onOkClick, text = 'OK').pack(side = 'top')
    Button(root, command=onSkipClick, text = 'SKIP').pack(side = 'top')

    

    root.mainloop()
    print ("result " + result)
    return result



def quit(_):
    global stopThread
    stopThread = True
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
