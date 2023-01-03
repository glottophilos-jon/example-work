import json
from urllib import request, parse
import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb
import os

#define behaviors for modnexus API requests
def nexusapi(apispec):
    #set headers for auth, replace "yourapikey" value
    myheaders = {"apikey":"yourapikey",
    "accept":"application/json"}

    rooturl = "https://api.nexusmods.com/v1/games/skyrimspecialedition/"
    fullcall = rooturl + apispec

    #run request
    try:
        modreq = request.Request(fullcall, headers=myheaders)
        modresponse = request.urlopen(modreq)
    except Exception as e:
        errortext = "Something went wrong with the api call for " + apispec + ", this script will check again on reboot.\n" + str(e)
        err = mb.showerror("Skyrim Update Script", errortext)
        if err == "ok":
            exit()

    return modresponse

#create basic canvas with message
def canvasgen(maintext):
    #put together attributes of main window and launch
    global root
    root = tk.Tk()
    root.title("Skyrim Update Script")
    #root.iconbitmap("somefile.ico")
    window_width = 500
    screen_width = root.winfo_screenwidth()
    center_x = int(screen_width/2 - window_width / 2)
    root.geometry(f'{window_width}x200+{center_x}+200')
    canvas = tk.Canvas(root, width = 500)
    canvas.pack()
    canvas.create_text(window_width/2, 
        100, 
        text=maintext, 
        font=("TkDefaultFont", 11),
        width=400
    )

#define what happens with initial question
def popdialog():
    questiontext = "The currently installed version is " + currver + " and the new version is " + newver + ". Would you like to update?"
    check = mb.askquestion('Skyrim Update Script', questiontext)
    if check == 'yes':
        doupdate()
    else:
        root.destroy()

def doupdate():
    os.system("C:\\Users\\Public\\Desktop\\Vortex.lnk")

#open logfile and check version no.
try:
    logfile = open("D:\\Documents\\My Games\\Skyrim Special Edition\\SKSE\\skse64.log", "r")
    firstline = logfile.readline()
    contentsarr = firstline.split()
except Exception as e:
    errortext = "Something went wrong with checking the logfile for SKSE.\n" + str(e)
    err = mb.showerror("Skyrim Update Script", errortext)
    if err == "ok":
        exit()
        
logfile.close()

for section in contentsarr:
    if "version" in section:
        index = contentsarr.index(section) + 2
        currver = contentsarr[index]

#run call to check version no.
modjson = json.load(nexusapi("mods/30379.json"))
newver = modjson["version"]

if currver != newver:
    canvasgen("There is an update available for your installation of SKSE!")

    popdialog()
    root.mainloop()
