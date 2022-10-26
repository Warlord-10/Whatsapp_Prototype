from pathlib import Path
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog
import pickle
import os
import functions as fn
import shutil


class person():
    #Define the user
    def __init__(self):
        self.name=None
        self.mobile=None
        self.display_pic = None
        '''
        try:
            self.display_pic = "appdata//images//disp_pics//profilepic.jpeg"
        except:
            self.display_pic = "appdata//images//disp_pics//default.jpeg"
        ''' 
        
    def update_profile(self):
        pic=filedialog.askopenfilename(title="Select Image")
        shutil.copy(pic,'appdata//images//disp_pics//profilepic.jpeg'),
        #API.pics((30,30),APP.dp,'appdata//images//disp_pics//profilepic.jpeg')

    def verify(self):
        try:
            basic_data = open('appdata//userinfo.dat','rb')
            basic_data = pickle.load(basic_data)    
            self.mobile = basic_data["mobile"]
            self.name = basic_data["name"]
            return "Passed"
        except:
            return "Failed"



    '''def share(self):
        for x in list(app.online.keys()):
            try:
                pic='appdata//images//disp_pics//profilepic.jpeg'
                file_name=os.path.basename(pic)
                file=open(pic,'rb')

                byte=file.read(1024)
                client.message_array.append({'type':'upd','sender':user.mobile, 'msg':[user.mobile,byte], 'reciever':x})
                while len(byte)>0:
                    byte=file.read(2048)
                    client.message_array.append({'type':'upd','sender':user.mobile, 'msg':[user.mobile,byte], 'reciever':x})
                    time.sleep(0.1)
                file.close()
                client.message_array.append({'type':'upd','sender':user.mobile, 'msg':[user.mobile,'sent'], 'reciever':x})  
            except Exception as e:
                print(e)
    '''


