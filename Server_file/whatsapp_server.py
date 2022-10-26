import socket,threading,pickle,sql,time,os

def verification(mobile):
    if os.path.isfile(f'userdata//{mobile}.dat')==True:
        return('vrfd')  #verified
    else:
        return('unf')  #user not found

    
def creation(mobile,name):
    notfound=True
    for files in os.walk('userdata'):
        if files==f'{mobile}.dat':
            notfound==False
            return ('uae')  #user account exist
                
    if notfound==True:       
        f=open(f'userdata//{mobile}.dat','ab')
        pickle.dump([mobile,name],f)
        f.close()
        return ('accntcrtd')    #account created

def remove(no):
    #Remove a client
    server.CLIENTS[no].close()
    del server.CLIENTS[no]
    print(f'{no} DISCONNECTED')

def spam(data,reciever):
    #Send Message from server
    server.CLIENTS[reciever].send(pickle.dumps(data))



#create online server
class main_server:
    def __init__(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.ip=socket.gethostbyname(socket.gethostname())
        self.port=5555
        self.sock.bind((self.ip,self.port))
        self.sock.listen(5)
        self.CLIENTS={}
        self.BUFFER=1024*128
        print('[SERVER]: Initialisation Done')
        print('[SERVER]: Server started in',self.ip)

    def run(self):
        while True:
            conn,addr=self.sock.accept()
            cthread=threading.Thread(target=self.handler,args=(conn,addr))
            cthread.start()
        
    def handler(self,conn,addr):
        conn.send(pickle.dumps('[SERVER]: WELCOME TO WHATSAPP'))

        while True:
            try:
                initial=pickle.loads(conn.recv(2048))
                #[type,mobile,name]
                if initial["msg"]=='login':
                    reply=verification(initial["mobile"])
                    conn.send(pickle.dumps(reply))
                    if reply=='vrfd':    #[login,mobile]
                        self.CLIENTS[initial["mobile"]]=conn
                        print(f'{initial["mobile"]} CONNECTED')
                        break
                if initial["msg"]=='reg':
                    reply=creation(initial["mobile"],initial["name"])
                    conn.send(pickle.dumps(reply))
                    if reply == "accntcrtd":
                        print(f'{initial["mobile"]} REGISTERED')
            except:
                conn.close()
                break

        #Checks for previous messages
        for msgs in sql.show(initial["mobile"]):
            if msgs>():
                temp=['msg',str(msgs[0]),str(msgs[1]),str(msgs[2])]
                self.CLIENTS[initial[1]].send(pickle.dumps(temp))
                time.sleep(0.2)
        sql.remove(initial["mobile"])
        

        # MAIN LISTENER #
        while True:
            try:
                data=pickle.loads(conn.recv(self.BUFFER))
                print(data)

                if data['type']=='quit':
                    self.CLIENTS[data['sender']].close()
                    del self.CLIENTS[data['sender']]
                    print(data['sender'],'DISCONNECTED')
                    break

                elif data['type']=='pic' or data['type']=='msg' or data['type']=='part':
                    if data['reciever'] in list(self.CLIENTS.keys()): 
                        self.CLIENTS[data['reciever']].send(pickle.dumps(data))
                        print("data relayed to client")
                    else:
                        #time.sleep(1)
                        data["reciever"],data["sender"] = data["sender"],data["reciever"]
                        self.CLIENTS[data["reciever"]].send(pickle.dumps(data))
                        #sql.insert(data['sender'],data["msg"],data['reciever'])
                        print("data stored in database")

                '''elif data['type']=='upd':
                    for x in data['reciever']:
                        if x in list(self.CLIENTS.keys()): 
                            self.CLIENTS[x].send(pickle.dumps(data))
                        else:
                            sql.insert(data['sender'],data['msg'],x)'''

            except Exception as e:
                print(e)
                break
                 
                
            

'''------INITIALISATION------'''
    
if os.path.isdir("userdata")==False:
    os.mkdir("userdata")
    print('[SERVER]: Folder created')
else:
    print('[SERVER]: Folder check passed')
server=main_server()
threading.Thread(target=server.run).start() #permanent thread for new connections

