import pickle
import os
import time
import functions as fn
import socket
import threading


class startup():  
    print("[Connection]: Connection Initiated")  
    #it makes the connection
    def __init__(self,api_token=None):
        self.LINK = api_token

        self.SENDING_STACK = []
        self.RECEIVING_STACK = []
        self.ACTIVE = True

        self.MULTIPLIER = 128
        self.BUFFER=1024*self.MULTIPLIER
        
        #connection established
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server=socket.gethostbyname(socket.gethostname())
        self.port=5555
        self.addr=(self.server,self.port)
        self.client.connect(self.addr)
        print(pickle.loads(self.client.recv(2048)))

    def send(self,data):
        try:
            self.client.send(pickle.dumps(data))
            print("data sent")
        except:
            pass

    def sending(self):
        while self.ACTIVE:
            if self.SENDING_STACK>[]:
                print("data in sending stack")
                try:
                    temp_data = self.SENDING_STACK[0]
                    self.SENDING_STACK.pop(0)
                    if temp_data["type"] == "quit":
                        self.send(temp_data)
                        self.ACTIVE = False
                    if temp_data["type"] == "msg":
                        self.send(temp_data)
                        print("a message has been sent",len(self.SENDING_STACK))
                    else:
                        Sending_Thread = threading.Thread(target = self.file_send,args=[temp_data])
                        Sending_Thread.start()  
                        print("an image has be threaded and sent")      
                except socket.error as e:
                    print(e)

    def file_send(self,data,holder=None):
        try:
            basename = os.path.basename(data["msg"])

            f=open(data["msg"],"rb")
            data_read = f.read(1024)

            data["msg"] = ["start",basename]
            self.client.send(pickle.dumps(data))

            while len(data_read) > 0:
                data["type"] = "part"
                data["msg"] = [basename,data_read]
                self.client.send(pickle.dumps(data))
                data_read = f.read(1024*120)
                time.sleep(0.10)
            f.close()

            data["type"] = "pic"
            data["msg"] = ["end",basename]
            self.client.send(pickle.dumps(data))
            print("pic sended successfully")
        except Exception as e:
            return

    def send_reply(self,data):
        try:
            self.client.send(pickle.dumps(data))
            reply = (pickle.loads(self.client.recv(self.BUFFER)))
            return reply
        except socket.error as e:
            print(e)


    def recieve(self):
        while self.ACTIVE:
            print("Listening for new messages")
            try:
                temp_data=(pickle.loads(self.client.recv(self.BUFFER)))
                if temp_data["type"] == "msg":
                    fn.update(temp_data)
                    self.LINK.msg(temp_data)
                    print("a new message has been received")
                else:
                    self.RECEIVING_STACK.append(temp_data)
                    print("a pic received has been appended",len(self.RECEIVING_STACK))
            except:
                pass
    
    def execute(self):
        while self.ACTIVE:
            if self.RECEIVING_STACK>[]:
                try:
                    data = self.RECEIVING_STACK[0]
                    self.RECEIVING_STACK.pop(0)
                    if data["msg"][0] == "start":
                        print("got first part of pic")
                        file=open(f'appdata/images/{data["msg"][1]}','ab')
                        file.close()
                    elif data["type"]=="part":
                        file=open(f'appdata//images//{data["msg"][0]}','ab')
                        file.write(data['msg'][1])
                        file.close()
                    elif data['msg'][0]=='end':
                        print('pic received successfully')
                        fn.update({'type':'pic', 'sender':data['sender'], 'msg':f'appdata/images/{data["msg"][1]}', 'reciever':data["reciever"], 'dtime':data["dtime"]})
                        self.LINK.msg({'type':'pic', 'sender':data['sender'], 'msg':f'appdata/images/{data["msg"][1]}', 'reciever':data["reciever"], 'dtime':data["dtime"]})
                except:
                    pass   
                
            

            



