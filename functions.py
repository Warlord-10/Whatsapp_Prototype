from PIL import ImageTk, Image
from pathlib import Path
import pickle
import tkinter as tk

def getsize(name):
    return Path(name).stat().st_size

def getlines(name):
    f=open(name,'rb')
    x=0
    if getsize(name)>0:
        while True:
            try:
                l=pickle.load(f)
                x+=1
            except EOFError:
                return x
    else:
        return(0)
    f.close()

def opn(name,line=-1,start=0):
    f=open(name,'rb')
    try:
        x=start
        if getsize(name)>0:
            while True:
                try:
                    l=pickle.load(f)
                    if x==line:             #for specific line
                        return l
                    if line==(-1):          #for all lines
                        print(l)
                    x+=1
                except EOFError:
                    if line==-2:            #for last line
                        return(l)
                    break
    except FileNotFoundError:
        pass
    f.close()

def update(data):   #update the chat file
    file=open('appdata//chat.txt','ab')
    pickle.dump(data,file)
    file.close()

def open_pic(file):
    trial=tk.Toplevel()
    bg=Image.open(file)
    new=ImageTk.PhotoImage(bg)
    bglabel=tk.Label(trial,image=new)
    bglabel.photo=new
    bglabel.pack()




