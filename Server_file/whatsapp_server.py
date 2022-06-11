import socket,threading,pickle,sql,time,os

def verification(mobile):
    if os.path.isfile(f'userdata//{mobile}.dat')==True:
        return ('vrfd')  #verified
    else:
        return ('unf')  #user not found
    

def creation(mobile,name):
    notfound=True
    for files in os.walk('userdata'):
        if files==f'{mobile}.dat':
            return ('uae')  #user account exist
            notfound==False
                
    if notfound==True:       
        f=open(f'userdata//{mobile}.dat','ab')
        pickle.dump([mobile,name],f)
        return ('accntcrtd')    #account created
    f.close()

def remove(no):
    #Remove a client
    server.clients[no].close()
    del server.clients[no]
    print(f'{no} DISCONNECTED')

def spam(data,reciever):
    #Send Message from server
    server.clients[reciever].send(pickle.dumps(data))



#create online server
class main_server:
    def __init__(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.ip=socket.gethostbyname(socket.gethostname())
        self.port=5555
        self.sock.bind((self.ip,self.port))
        self.sock.listen(5)
        self.clients={}
        self.BUFFER=1024*32
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
                if initial[0]=='login':
                    reply=verification(initial[1])
                    conn.send(pickle.dumps(reply))
                    if verification(initial[1])=='vrfd':    #[login,mobile]
                        self.clients[initial[1]]=conn
                        print(f'{initial[1]} CONNECTED')
                        break
                if initial[0]=='reg':
                    reply=creation(initial[1],initial[2])
                    conn.send(pickle.dumps(reply))
            except:
                conn.close()


        for msgs in sql.show(initial[1]):
            if msgs>():
                temp=['msg',str(msgs[0]),str(msgs[1]),str(msgs[2])]
                self.clients[initial[1]].send(pickle.dumps(temp))
                time.sleep(0.2)
        sql.remove(initial[1])
        

        # MAIN LISTENER #
        while True:
            try:
                data=pickle.loads(conn.recv(self.BUFFER))
                print(data['sender'],data['type'])


                if data['type']=='quit':
                    self.clients[data['sender']].close()
                    del self.clients[data['sender']]
                    print(data['sender'],'DISCONNECTED')
                    break

                elif data['type']=='pic' or data['type']=='msg' or data['type']=='upd':
                    if data['reciever'] in list(self.clients.keys()): 
                        self.clients[data['reciever']].send(pickle.dumps(data))
                        print("data relayed to client")
                    else:
                        sql.insert(data['sender'],data,data['reciever'])
                        print("data stored in database")

                '''elif data['type']=='upd':
                    for x in data['reciever']:
                        if x in list(self.clients.keys()): 
                            self.clients[x].send(pickle.dumps(data))
                        else:
                            sql.insert(data['sender'],data['msg'],x)'''

            except Exception as e:
                print(e)  
                
            

'''------INITIALISATION------'''
    
if os.path.isdir("userdata")==False:
    os.mkdir("userdata")
    print('[SERVER]: Folder created')
else:
    print('[SERVER]: Folder check passed')
    
server=main_server()
threading.Thread(target=server.run).start() #permanent thread for new connections

