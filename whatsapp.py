import tkinter as tk
import pickle
import csv
import os
import time
import shutil
from pathlib import Path
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog
import functions as fn
import socket
import threading


'''------COLOURS------'''
head='#2a2e33'
you_send='#056063'
they_send='#272d30'
chat_button='#131c21'

'''--------BASIC FUNCTIONS---------'''



'''--------CLASS FUNCTIONS---------'''
def pic_send(self):
    pic=filedialog.askopenfilename(title='Select File')#filetypes=('png files','*.png'))
    if pic is not None:
        print(pic)
        
        counter=2
        start_time=time.time()
        try:
            file_name=os.path.basename(pic)
            file=open(pic,'rb')
            
            byte=file.read(1024)
            client.message_array.append({'type':'pic','sender':user.mobile, 'msg':[file_name,byte], 'reciever':self.mobile})
            while len(byte)>0:
                counter+=1
                byte=file.read(1024*16)
                client.message_array.append({'type':'pic','sender':user.mobile, 'msg':[file_name,byte], 'reciever':self.mobile})
                #time.sleep(0.1)
            file.close()

            ct=f"{time.localtime().tm_hour}:{time.localtime().tm_min}"
            info={'type':'pic','sender':user.mobile, 'msg':[file_name,'sent'], 'reciever':self.mobile, 'dtime':ct}  
            client.message_array.append(info)

        except Exception as e:
            print(e)

        end_time=time.time()
        print(f"Time Taken to send {pic} is {end_time-start_time} and {counter} relays")
        print(client.message_array)

        info['msg']=[pic,'sent']
        API.msg(info)
        fn.update(info)

    
def msgsend(self):
    #FORMAT: {'type':msg/pic, 'sender':int, 'msg':message, 'reciever':int, 'dtime':time}
    data=self.msg.get()
    self.msg.set('')
    #self.chat_canvas2.yview_moveto(1.0)

    ct=f"{time.localtime().tm_hour}:{time.localtime().tm_min}"
    info={'type':'msg', 'sender':user.mobile, 'msg':data, 'reciever':self.mobile, 'dtime':ct}
    API.msg(info)
    client.send(info)
    fn.update(info)

def pics(size,but_name,pic=None,**kwargs):
    #Add picture to a button
    if pic is None:
        pic=filedialog.askopenfilename(title='Select File')
    bg=Image.open(pic)
    rg=bg.resize(size,Image.ANTIALIAS)
    dp=ImageTk.PhotoImage(rg)
    but_name.photo=dp
    but_name['image']=dp

    try:
        if kwargs['fileset']==True:
            shutil.copy(pic,'appdata//images//disp_pics//profilepic.jpeg')
    except:
        pass

'''---------BODY--------'''           
class body():    
    #home page
    def __init__(self):
        self.window=tk.Tk()
        WIDTH =self.window.winfo_screenwidth()
        HEIGHT =self.window.winfo_screenheight()
        self.window.title('Buddies')
        
        self.window.geometry('800x600')
        self.window.resizable(True,True)

        #Primary Frame
        self.dad_frame=tk.Frame(self.window,bg='grey')
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

class app():
    #main driver
    def __init__(self,parent):

        self.online={}  #{mobile:name}
        self.contacts() #name of a function
        self.container={}


        #loading all the contacts
        for x in self.online:
            y=boo(x,self.online[x],parent)    #(mobile,name,self)
            self.container[x]=y


        #setting up the display picture
        self.dp=tk.Button(parent.info_frame,command=self.setting)
        self.dp.pack(padx=10,expand=True,anchor='w')
        try:
            API.pics((30,30),self.dp,'appdata//images//disp_pics//profilepic.jpeg')
        except:
            pass
            #pics((30,30),self.dp,'appdata//images//disp_pics//default.jpeg')

        
    #loading the contacts in online dict
    def contacts(self):     
        f=open('contacts.csv','r')
        read=csv.reader(f)
        for row in read:
            self.online[row[0]]=row[1]  #[mobile,name]
            
    def load(self):       
        trials=fn.getlines('appdata//chat.txt')
        #['msg',someone,message,us]
        #['msg',us,message,someone]
        for abcd in range(0,trials):
            data=fn.opn('appdata//chat.txt',line=abcd)
            API.msg(data)

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
        b3.pack()


class boo():    
    #frame of each chat
    def __init__(self,mobile,page,parent):

        self.mobile=mobile
        self.name=page
        
        self.b1=tk.Button(parent.frame2,text=self.name,command= lambda : self.show(),bg='pink')
        self.b1.pack(fill='x',ipady=15)
        self.b1.pack_propagate(0)

        #parent base frame containing all chat elements
        self.base=tk.Frame(parent.chat_frame)
        self.base.grid(row=0,column=0,sticky='nwse')
        self.base.pack_propagate(0)
        self.base.lower()


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

        send=tk.Button(lower,text='PIC',command= lambda :pic_send(self))
        send.pack(side='left',padx=5)
        
        self.msg=tk.StringVar()
        entry=tk.Entry(lower,textvariable=self.msg,font='default 15')
        entry.pack(side='left',padx=5,expand=True,fill='x')

        send=tk.Button(lower,text='SEND',width=8,command= lambda :msgsend(self))
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

    def show(self):
        self.base.tkraise()


class startup():    
    #it makes the connection
    def __init__(self):
        
        #connection established
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server=socket.gethostbyname(socket.gethostname())
        self.port=5555
        self.addr=(self.server,self.port)
        self.client.connect(self.addr)
        self.BUFFER=1024*32
        print(pickle.loads(self.client.recv(2048)))

        self.message_array=[] 

    def relay(self):
        while True:
            if len(self.message_array)>0:
                try:
                    self.send(self.message_array[0])
                    self.message_array.pop(0)
                except:
                    pass
                #time.sleep(0.1)

    def send(self,data):
        '''Default format: [Sender,message,receiver]'''
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            print(e)

    def recieve(self):
        while True:
            try:
                data=(pickle.loads(self.client.recv(self.BUFFER)))
                print("got data")

                if data['type']=='pic':
                    if data['msg'][1]=='sent':
                        print('pic complete')
                        API.msg(data)
                        fn.update({'type':'pic', 'sender':data['sender'], 'msg':f'appdata//images//{data["msg"][0]}', 'reciever':data["reciever"]})
                    else:
                        file=open(f'appdata//images//{data["msg"][0]}','ab')
                        file.write(data['msg'][1])
                        file.close()
                        
                elif data['type']=='msg':
                    print(data)
                    API.msg(data)
                    print("msg built")
                    fn.update(data)

                '''
                elif data['type']=='upd':
                    if data['msg'][1]=='sent':
                        print('pic complete')
                        pics((30,30),app.container[data['sender']].dp,f'appdata//images//disp_pics//{data["msg"][0]}')
    
                    else:
                        file=open(f'appdata//images//disp_pics//{data["msg"][0]}','ab')
                        file.write(data['msg'][1])
                        file.close()'''
            except:
                break


class UI():
    def msg(self,kwargs):
        print("API called")
        #FORMAT: {'type':msg/pic, 'sender':int, 'msg':message, 'reciever':int, 'dtime':time}
        base_frame=tk.Frame(APP.container[kwargs['reciever']].top_frame,bg='#056063')
        base_frame.pack(anchor='e',padx=5,pady=2)
        print("baseframe done")

        if kwargs['type']=='msg':
            msg=tk.Label(base_frame,text=kwargs['msg'],bg='#056063',fg='white',font='default 16',wraplength=350)
            msg.pack(side="left")
            print("msg done")
            if kwargs['sender']!=str(user.mobile):
                base_frame['parent']=APP.container[kwargs['sender']].top_frame
                base_frame['anchor']="w"
                msg['bg']='#272d30'

        elif kwargs['type']=='pic':
            holder=tk.Button(base_frame,command= lambda: fn.open_pic(kwargs['msg'][0]))
            self.pics((300,300),holder,kwargs['msg'][0])
            holder.pack(padx=5,pady=5)
            if kwargs['sender']!=str(user.mobile):
                base_frame['master']=APP.container[kwargs['sender']].top_frame
                base_frame['anchor']='w'
                base_frame['bg']='#272d30'
        
        timelabel=tk.Label(base_frame,text=kwargs['dtime'],font="default 8",bg=base_frame['bg'])
        timelabel.pack(side="right",anchor="s")

    def pics(self,size,but_name,pic):
        #Add picture to a button
        bg=Image.open(pic)
        rg=bg.resize(size,Image.ANTIALIAS)
        dp=ImageTk.PhotoImage(rg)
        but_name.photo=dp
        but_name['image']=dp

    '''
    def update_dp(self,pic,win=None):
        if pic is None:
            pic=filedialog.askopenfilename(title='Select Image')
            self.pics((30,30),user.dp,pic)
        else:
            self.pics((30,30),win,pic)
            '''
    

class person():
    #Define the user
    def __init__(self,name,mobile):
        self.name=name
        self.mobile=mobile
        
    def update_profile(self):
        pic=filedialog.askopenfilename(title="Select Image")
        shutil.copy(pic,'appdata//images//disp_pics//profilepic.jpeg'),
        API.pics((30,30),APP.dp,'appdata//images//disp_pics//profilepic.jpeg')

    def share(self):
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


class login():
    #login page
    def __init__(self):
        self.login_frame=tk.Frame(BODY.chat_frame,bg='pink')
        self.login_frame.grid(row=0,column=0)

        tk.Label(self.login_frame,text='LOGIN',font='default 20').grid(row=0,column=0,pady=10,columnspan=2)
    
        tk.Label(self.login_frame,text='Enter Mobile No',font='default 12').grid(row=1,column=0,pady=10,padx=10)
        self.mob_no=tk.StringVar()
        mob=tk.Entry(self.login_frame,textvariable=self.mob_no,font='default 12').grid(row=1,column=1,padx=10)
        
        tk.Label(self.login_frame,text='Enter Name',font='default 12').grid(row=2,column=0,pady=10,padx=10)
        self.name_no=tk.StringVar()
        mob=tk.Entry(self.login_frame,textvariable=self.name_no,font='default 12').grid(row=2,column=1,padx=10)
        
        submit=tk.Button(self.login_frame,text='SUBMIT',command=self.register).grid(row=3,column=0,pady=10,columnspan=2)

        self.b1=tk.Button(self.login_frame,bg='white',command = lambda: self.pic_change())
        self.b1.grid(row=0,column=3,sticky='ns',rowspan=4,pady=10,padx=10)
        
        BODY.chat_frame.columnconfigure(0,weight=1)
        BODY.chat_frame.rowconfigure(0,weight=1)

    def pic_change(self):
        self.pic=filedialog.askopenfilename(title='Select File')
        bg=Image.open(self.pic)
        rg=bg.resize((300,300),Image.ANTIALIAS)
        dp=ImageTk.PhotoImage(rg)
        self.b1.photo=dp
        self.b1['image']=dp

    def register(self):
        name=str(self.name_no.get())
        mobile=str(self.mob_no.get())

        client.send(['reg',mobile,name])
        reply=pickle.loads(client.client.recv(2048))

        if reply=='accntcrtd':
            initial=open('appdata//userinfo.dat','wb')
            pickle.dump([mobile,name],initial)
            initial.close()

            f=open('appdata//chat.txt','wb')
            f.close()

            try:
                shutil.copy(f'{self.pic}','appdata//images//disp_pics//profilepic.jpeg')
            except:
                pass
            self.login_frame.destroy()

            global APP,user
            user=person(name,mobile)
            APP=app(BODY)
            threading.Thread(target=client.recieve).start()
            threading.Thread(target=client.relay).start()
            
    

# DRIVER CODE
API=UI()

BODY=body()
client=startup()

if os.path.isdir("appdata")==False:
    os.mkdir("appdata")
    os.mkdir("appdata//images")
    os.mkdir("appdata//images//disp_pics")
try:
    initial=open('appdata//userinfo.dat','rb')
    print("[APP]: Info Check Passed")

    temp=pickle.load(initial)
    user=person(temp[1],temp[0])
    print("[APP]: User Created")
    print("[APP]:",user.name,user.mobile)

    client.send(['login',user.mobile,user.name])
    reply=pickle.loads(client.client.recv(2048))
    print("[APP]: Server Validation Complete")

    if reply=='vrfd':
        APP=app(BODY)
        print("[APP]: Application Initiated")
        APP.load()
        print("[APP]: Loading Complete")
        threading.Thread(target=client.recieve).start()
        threading.Thread(target=client.relay).start()
        print("[APP]: All Check Completed")


except Exception as e:
    print(e)
    setup=login()

BODY.window.mainloop()
client.send({'type':'quit','sender':user.mobile})
quit()

