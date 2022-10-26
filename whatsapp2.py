import tkinter as tk
import pickle
import csv
import os
import time

import Connection
import Client

from pathlib import Path
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog
from multiprocessing import Process
from threading import Thread
import functions as fn





'''---------BODY--------'''           
class body():    
    def __init__(self):
        #Universal constant
        self.CURR_CHAT = None
        self.CONTAINER={}
        self.LINK=None
        self.WINDOW=tk.Tk()

        
        WIDTH =self.WINDOW.winfo_screenwidth()
        HEIGHT =self.WINDOW.winfo_screenheight()
        self.WINDOW.title('Buddies')
        self.WINDOW.geometry('800x600')
        self.WINDOW.resizable(True,True)

        #Primary Frame
        self.dad_frame=tk.Frame(self.WINDOW,bg='grey')
        self.dad_frame.pack(expand=True,fill='both')
        
        # Two Main Frames
        list_frame=tk.Frame(self.dad_frame)
        list_frame.grid(row=0,column=0,sticky='NSEW')
        list_frame.pack_propagate(0)
       
        self.chat_frame=tk.Frame(self.dad_frame,bg='#272c31')
        self.chat_frame.grid(row=0,column=1,sticky='NSEW')
        self.chat_frame.grid_propagate(0)

        self.dad_frame.columnconfigure(0,weight=1)
        self.dad_frame.columnconfigure(1,weight=3)
        self.dad_frame.rowconfigure(0,weight=1)
                
        self.info_frame=tk.Frame(list_frame,bg='green',height=50)
        self.info_frame.pack(fill='x')
        self.info_frame.pack_propagate(0)

        chat_canvas=tk.Canvas(list_frame)
        self.frame2=tk.Frame(chat_canvas)   #frame where all elements are placed
        scroll=ttk.Scrollbar(list_frame,orient='vertical',command=chat_canvas.yview)
        chat_canvas.configure(yscrollcommand=scroll.set)

        def onFrameConfigure(event):
            chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))
        def onCanvasConfigure(event):
            width = event.width - 4
            chat_canvas.itemconfigure("my_tag", width=width)

        self.frame2.bind("<Configure>",onFrameConfigure)
        chat_canvas.bind("<Configure>",onCanvasConfigure)
        scroll.pack(side='right',fill='y')
        chat_canvas.pack(side='left',fill='both',expand=True)
        chat_canvas.create_window((0,0), window=self.frame2, anchor="nw",tags='my_tag')

        self.chat_frame.columnconfigure(0,weight=1)
        self.chat_frame.rowconfigure(0,weight=1)

    def update(self,pointer):
        if self.CURR_CHAT != None:
            self.CURR_CHAT.base.grid_forget()
        pointer.base.grid(row=0,column=0,sticky='nwse')
        self.CURR_CHAT=pointer
        print("Current Chat: ",self.CURR_CHAT)

    def initalize(self):        
        f=open("C:/Users/91931/OneDrive/Desktop/Deep/WhatsApp/contacts.csv",'r')
        read=csv.reader(f)
        for row in read:
            y=boo(row[0],row[1],self)    #(mobile,name,self)
            self.CONTAINER[row[0]]=y


        #setting up the display picture
        self.dp=tk.Button(self.info_frame)#,command=self.setting)
        self.dp.pack(padx=10,expand=True,anchor='w')
        try:
            API.pics((30,30),self.dp,'appdata//images//disp_pics//profilepic.jpeg')
        except:
            pass
            #pics((30,30),self.dp,'appdata//images//disp_pics//default.jpeg')
    '''            
    def load(self):       
        trials=fn.getlines('appdata//chat.txt')
        #['msg',someone,message,us]
        #['msg',us,message,someone]
        for abcd in range(0,trials):
            data=fn.opn('appdata//chat.txt',line=abcd)
            API.msg(data)'''
'''
    def setting(self):
        self.prof_frame=tk.Frame(BODY.dad_frame,bg='red')
        self.prof_frame.grid(row=0,column=0,sticky='NESW')
        self.prof_frame.pack_propagate(0)

        b1=tk.Button(self.prof_frame,command= user.update_profile)        
        b1.pack()
        API.pics((50,50),b1,'appdata//images//disp_pics//profilepic.jpeg')

        b2=tk.Button(self.prof_frame,text='close',command=self.prof_frame.destroy)
        b2.pack()

        b3=tk.Button(self.prof_frame,text='Clear Chat',command= lambda: open('appdata//chat.txt','wb'))
        b3.pack()'''


class boo():    
    #frame of each chat
    def __init__(self,mobile,name,parent):

        self.mobile=mobile
        self.name=name
        
        self.b1=tk.Button(parent.frame2,text=self.name,command= lambda : parent.update(self),bg='pink')
        self.b1.pack(fill='x',ipady=15)
        self.b1.pack_propagate(0)

        #parent base frame containing all chat elements
        self.base=tk.Frame(parent.chat_frame)
        self.base.grid(row=0,column=0,sticky='nwse')
        self.base.pack_propagate(0)
        self.base.grid_forget()


        head_frame=tk.Frame(self.base,bg='#075e54',height=50)
        head_frame.pack(fill='x')
        head_frame.pack_propagate(0)

        self.dp=tk.Button(head_frame)
        self.dp.pack(padx=10,side='left')
        try:
            API.pics((30,30),self.dp,f'appdata//images//disp_pics//{self.mobile}_dp.jpeg')
        except:
            pass

        tk.Label(head_frame,text=self.name,font='default 12').pack(padx=10,side='left')

        lower=tk.Frame(self.base,bg='#075e54',height=50)
        lower.pack(side='bottom',ipady=5,fill='x')
        lower.pack_propagate(0)

        send=tk.Button(lower,text='PIC',command= lambda :API.create_msg("pic"))
        send.pack(side='left',padx=5)
        
        self.msg=tk.StringVar()
        entry=tk.Entry(lower,textvariable=self.msg,font='default 15')
        entry.pack(side='left',padx=5,expand=True,fill='x')

        send=tk.Button(lower, text='SEND', width=8, command= lambda :API.create_msg("msg"))  
        send.pack(side='left',padx=5)
        
        
        self.chat_canvas2=tk.Canvas(self.base,bg='#ece5dd')
        self.top_frame=tk.Frame(self.chat_canvas2,bg='#ece5dd') #frame where all elements will be placed
        scroll=ttk.Scrollbar(self.base,orient='vertical',command=self.chat_canvas2.yview)
        self.chat_canvas2.configure(yscrollcommand=scroll.set)

        def onFrameConfigure(event):
            self.chat_canvas2.configure(scrollregion=self.chat_canvas2.bbox("all"))
        def onCanvasConfigure(event):
            width = event.width - 4
            self.chat_canvas2.itemconfigure("my_tag", width=width)

        self.top_frame.bind("<Configure>",onFrameConfigure)
        self.chat_canvas2.bind("<Configure>",onCanvasConfigure)
        scroll.pack(side='right',fill='y')
        self.chat_canvas2.pack(side='left',fill='both',expand=True)
        self.chat_canvas2.create_window((0,0), window=self.top_frame, anchor="nw",tags='my_tag')


class UI():
    def create_msg(self,format):
        #FORMAT: {'type':msg/pic, 'sender':int, 'msg':message, 'reciever':int, 'dtime':time}
        local_time=f"{time.localtime().tm_hour}:{time.localtime().tm_min}"
        raw_data = ""

        if format == "msg":
            message = BODY.CURR_CHAT.msg
            raw_data = {"type":"msg", "sender":str(USER.mobile), "msg":message.get(), "reciever":BODY.CURR_CHAT.mobile, "dtime":local_time}
            message.set(" ")
            print("chat raw_data is created")
        
            self.msg(raw_data)
            print("chat has been made: .msg function")

            fn.update(raw_data)
            print("chat raw_data is updated: .update function")

            CONNECTION.SENDING_STACK.append(raw_data)
            print("raw_data from client appended")

            
        elif format == "pic":
            pic_filename=filedialog.askopenfilename(title='Select File')
            print(pic_filename)
            raw_data = {"type":"pic", "sender":str(USER.mobile), "msg":pic_filename, "reciever":BODY.CURR_CHAT.mobile, "dtime":local_time}
            print("image raw_data is created")

            CONNECTION.SENDING_STACK.append(raw_data)
            print("raw_data from client appended")

            self.msg(raw_data)
            print("image has been made: .msg function")

            fn.update(raw_data)
            print("image raw_data is updated: .update function")

            
        
         
    def msg(self,kwargs):
        #It makes the message box of every message
        base_frame=""

        if kwargs["sender"] == str(USER.mobile):
            base_frame=tk.Frame(BODY.CONTAINER[kwargs['reciever']].top_frame,bg='#056063')
            base_frame.pack(anchor='e',padx=5,pady=2)
        else:
            base_frame=tk.Frame(BODY.CONTAINER[kwargs['sender']].top_frame)
            base_frame.pack(anchor='w',padx=5,pady=2)


        if kwargs['type']=='msg':
            msg=tk.Label(base_frame,text=kwargs['msg'],bg=base_frame["background"],fg='black',font='default 16',wraplength=350)
            msg.pack(side="left")

        elif kwargs['type']=='pic':
            holder=tk.Button(base_frame,command= lambda: fn.open_pic(kwargs['msg']))
            self.pics((300,300),holder,kwargs['msg'])
            holder.pack(padx=5,pady=5)
            
        timelabel=tk.Label(base_frame,text=kwargs['dtime'],font="default 8",bg=base_frame['bg'])
        timelabel.pack(side="right",anchor="s")

    def pics(self,size,but_name,pic):
        #Add picture to a button
        bg=Image.open(pic)
        rg=bg.resize(size,Image.Resampling.LANCZOS)
        dp=ImageTk.PhotoImage(rg)
        but_name.photo=dp
        but_name['image']=dp


class login():
    #login page
    def __init__(self,parent):

        self.login_frame=tk.Frame(parent.chat_frame,bg='pink')
        self.login_frame.grid(row=0,column=0)

        self.name_no=tk.StringVar()
        self.mob_no=tk.StringVar()
        self.disp_pic = None

        tk.Label(self.login_frame,text='LOGIN',font='default 20').grid(row=0,column=0,pady=10,columnspan=2)

        tk.Label(self.login_frame,text='Enter Name',font='default 12').grid(row=1,column=0,pady=10,padx=10)
        mob=tk.Entry(self.login_frame,textvariable=self.name_no,font='default 12').grid(row=1,column=1,padx=10)
        tk.Label(self.login_frame,text='Enter Mobile No',font='default 12').grid(row=2,column=0,pady=10,padx=10)
        mob=tk.Entry(self.login_frame,textvariable=self.mob_no,font='default 12').grid(row=2,column=1,padx=10)
        
        
        submit=tk.Button(self.login_frame,text='SUBMIT',command=self.register).grid(row=3,column=0,pady=10,columnspan=2)
        self.b1=tk.Button(self.login_frame,bg='white',command = lambda: self.pic_change())
        self.b1.grid(row=0,column=3,sticky='ns',rowspan=4,pady=10,padx=10)
        
        parent.chat_frame.columnconfigure(0,weight=1)
        parent.chat_frame.rowconfigure(0,weight=1)

    def pic_change(self):
        self.disp_pic=filedialog.askopenfilename(title='Select File')
        bg=Image.open(self.pic)
        rg=bg.resize((300,300),Image.ANTIALIAS)
        dp=ImageTk.PhotoImage(rg)
        self.b1.photo=dp
        self.b1['image']=dp

    def register(self):
        name=str(self.name_no.get())
        mobile=str(self.mob_no.get())
        raw_data = {"msg":"reg", "mobile":mobile, "name":name}
        sent_to_login = CONNECTION.send_reply(raw_data)

        if sent_to_login == "accntcrtd":
            initial=open('appdata//userinfo.dat','wb')
            pickle.dump({"mobile":mobile, "name":name},initial)
            initial.close()
            f=open('appdata//chat.txt','wb')
            f.close()
            self.login_frame.destroy()

            USER.name = self.name_no
            USER.mobile = self.mob_no
            if CONNECTION.send_reply({"msg":"login", "mobile":USER.mobile}) == "vrfd":
                print("All Check PASSED")
                BODY.initalize()
            else:
                print("Access Failed: User not verified")
        
        
        
# DRIVER CODE #
if __name__ == "__main__":
    BODY = body()
    API = UI()
    #BODY.LINK = API
    CONNECTION = Connection.startup(API)
    USER = Client.person()

    if USER.verify() == "Passed":
        if CONNECTION.send_reply({"msg":"login", "mobile":USER.mobile}) == "vrfd":
            print("ALL CHECK PASSED AND VERIFIED")
            print(USER.name,USER.mobile)
            
            BODY.initalize()
            LISTENING = Process(target = CONNECTION.recieve)
            LISTENING.daemon = True
            LISTENING.start()

            SENDING = Process(target = CONNECTION.sending)
            SENDING.daemon = True
            SENDING.start()

            EXECUTING = Process(target = CONNECTION.execute)
            EXECUTING.daemon = True
            EXECUTING.start()
        else:
            print("Access Failed: User not verified")
    else:
        if os.path.isdir("appdata")==False:
            os.mkdir("appdata")
            os.mkdir("appdata//images")
            os.mkdir("appdata//images//disp_pics")
        login(BODY)


    BODY.WINDOW.mainloop()
    
    print("killing all the threads and processes")
    print(LISTENING.is_alive())

    print(SENDING.is_alive())

    print(EXECUTING.is_alive())

    CONNECTION.SENDING_STACK.append({'type':'quit','sender':USER.mobile})
    print("quit command sent")
    quit()

