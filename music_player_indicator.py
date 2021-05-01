
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
from gi.repository import GObject
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from os.path import join, dirname
from dotenv import load_dotenv
from tkinter import *
import json
from pygame import mixer
import random




APPINDICATOR_ID = 'pythonmusicplayerindicator'

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('/home/tharsanan/Projects/AppIndicatorsUbuntu/music.png'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    
    indicator.set_menu(build_menu())
    acgroup = gtk.AccelGroup()
    indicator.add_accel_group(acgroup)
    notify.init(APPINDICATOR_ID)
    gtk.main()


def check_music_player_status():
    global play_songs_flag
    # print("check", is_paused, play_songs_flag, mixer.music.get_busy(), ((not is_paused) and play_songs_flag and (not mixer.music.get_busy())), not mixer.music.get_busy())
    if ((not is_paused) and play_songs_flag and (not mixer.music.get_busy())):
        next_action(None)
    return True


def fill_songs_list():
    global songs_list
    for file in os.listdir(songs_folder_abs_path):
        if file.endswith(".ogg"):
            songs_list.append(file)


def play_song(song):
    global songs_folder_abs_path
    mixer.music.load(songs_folder_abs_path + song)
    mixer.music.play()

def resume_song():
    mixer.music.unpause()

def pause_song() :
    mixer.music.pause()

def build_menu():
    menu = gtk.Menu()
    
    
    item_suspend = gtk.RadioMenuItem('Set lid to suspend')
    menu.append(item_suspend)

    item_nothing = gtk.RadioMenuItem('Set lid to nothing')
    menu.append(item_nothing)

    item_suspend.set_active(True)

    item_suspend.join_group(item_nothing)

    sep = gtk.SeparatorMenuItem()
    menu.append(sep)

    start_menu = gtk.MenuItem('START')
    start_menu.connect('activate', start_action)
    menu.append(start_menu)

    pause_menu = gtk.MenuItem('PAUSE')
    pause_menu.connect('activate', pause_action)
    menu.append(pause_menu)

    resume_menu = gtk.MenuItem('RESUME')
    resume_menu.connect('activate', resume_action)
    menu.append(resume_menu)

    # Seperator

    sep = gtk.SeparatorMenuItem()
    menu.append(sep)

    prev_menu = gtk.MenuItem('PREV')
    prev_menu.connect('activate', prev_action)
    menu.append(prev_menu)

    prev_menu = gtk.MenuItem('NEXT')
    prev_menu.connect('activate', prev_action)
    menu.append(prev_menu)

    suffle_menu = gtk.MenuItem('SUFFLE')
    suffle_menu.connect('activate', suffle_action)
    menu.append(suffle_menu)

    menu.show_all()
    return menu

def start_action(_):
    global play_songs_flag
    play_songs_flag = True
    play_song(songs_list[current_song_index])
    return

def pause_action(_):
    global is_paused
    if (not is_paused):
        is_paused = True
        pause_song()
    return

def resume_action(_):
    global is_paused
    if (is_paused):
        resume_song()
        is_paused = False

def prev_action(_):
    global current_song_index
    global songs_list
    if(current_song_index == 0) :
        current_song_index = len(songs_list) - 1
    else:
        current_song_index = current_song_index - 1
    play_song(songs_list[current_song_index])
    return

def next_action(_):
    global current_song_index
    global songs_list
    if(current_song_index == len(songs_list) - 1) :
        current_song_index = 0
    else:
        current_song_index = current_song_index + 1
    play_song(songs_list[current_song_index])
    return

def suffle_action(_):
    global songs_list
    random.shuffle(songs_list)
    next_action(None)

def quit(_):
    notify.uninit()
    gtk.main_quit()


mixer.init()
global song_list
global current_song_index
global play_songs_flag
global is_paused
is_paused = False
play_songs_flag = False
current_song_index = -1
songs_list = []
songs_folder_abs_path = "/home/tharsanan/Music/python-player/"
songs_data_file_name = "songs_data.json"

GObject.timeout_add(2000, check_music_player_status)


with open(songs_folder_abs_path + songs_data_file_name) as f:
  songs_data = json.load(f)

fill_songs_list()

keys = list(songs_data.keys())

for key in keys:
    if (key in songs_list):
        continue
    else :
        songs_data.pop(key, None)
        

keys = list(songs_data.keys())

for song in songs_list:
    if (song in keys) :
        continue
    else :
        song_detail = {
            "name" : song,
            "watched_time" : 0,
            "genre" : "None"
        }
        songs_data[song] =  song_detail


with open(songs_folder_abs_path + songs_data_file_name, 'w') as json_file:
    json.dump(songs_data,  json_file, indent = 4,)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
