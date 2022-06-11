import pickle
from pathlib import Path

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
    f.close()

def getsize(name):
    return Path(name).stat().st_size

def opn(name,line=-1,start=0):
    f=open(name,'rb')
    x=start
    if getsize(name)>0:
        while True:
            try:
                l=pickle.load(f)
                if x==line:             #for specific line
                    return l
                if line==-1:
                    print(l)
            except EOFError:
                if line==-2:            #for last line
                    return(l)
                break
    f.close()

