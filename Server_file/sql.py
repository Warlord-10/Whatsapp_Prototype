print('Welcome To SQL Module')
print('---------------------')
print('                     ')


import mysql.connector
mydb = mysql.connector.connect(host="localhost",user="root",password="pass")
mycursor=mydb.cursor()


'''----------------------------------'''
def createdb():
    mycursor.execute('create database SERVER')
    mycursor.execute('use SERVER')
    mycursor.execute('create table BUFFER (SENDER char(10), MSG MEDIUMTEXT, RECV char(10))')
    print('[SERVER]: DataBase Created')

def dropdb():
    mycursor.execute('drop database SERVER')
    print('[SERVER]: DataBase Deleted')
    
def show(recv='all'):
    if recv=='all':
        mycursor.execute(f'select*from buffer')
    else:
        mycursor.execute(f'select*from buffer where RECV={recv}')
    myresult=list(mycursor.fetchall(),)
    return(myresult)

def insert(sender,msg,recv):
    sql="INSERT INTO BUFFER (SENDER,MSG,RECV) VALUES (%s, %s, %s)"
    val=(sender,msg,recv)
    mycursor.execute(sql,val)
    mydb.commit()

def remove(recv):
    mycursor.execute(f'DELETE from BUFFER where RECV={recv}')
    mydb.commit()
'''----------------------------------'''


try:
    mycursor.execute('use SERVER')
    print('[SERVER]: Database Online')
except Exception:
    #dropdb()
    createdb()

#insert('9911792465','sql test3','1234567890')
#insert('1234567890','sql test3','9911792465')

