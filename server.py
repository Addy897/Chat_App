import socket
import threading
import sys
import os

class Server:
    def __init__(self,host,port):
        self.socketserver = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
        self.clients=[]
        self.names=dict()
        name = socket.gethostname()
        self.socketserver.bind((host,port))
        self.socketserver.listen(5)
        print(f"[+] Chat Server Started at {host}:{port}")
        while True:
            try:
                client,addr=self.socketserver.accept()
                
                if(client not in self.clients):
                    self.clients.append(client)
                    self.sendAll(bytes(f"{len(self.clients)}-",'UTF-8'))
                    fThread = threading.Thread(target=self.handle,args=(client,))
                    fThread.daemon = True
                    fThread.start()
            except Exception as e:
                print(f"[-] {e}")
    
    
              
    def sendAll(self,msg,n=None):
                for c in self.clients:
                    if(c!=n):
                        c.send(msg)
    def handle(self,c):
            try:
                addr=c.getpeername()
                if(addr[0] not in self.names.keys()):
                    print(f"[+] {addr[0]} joined")
                    c.send(bytes(f"{len(self.clients)}-Server: Please Tell Your Name",'UTF-8'))
                    name=c.recv(1024).decode()
                   
                    while(not name.isalnum()  and name not in self.names.values()):
                        c.send(bytes(f"{len(self.clients)}-Server: Please Chose Another Name",'UTF-8'))
                        name=c.recv(1024).decode()
                    self.names[addr[0]]=name
                    print(f"[+] {addr[0]} is {name}")
                else:
                    name=self.names.get(addr[0])
                    c.send(bytes(f"{len(self.clients)}-Server: Welcome {name}",'UTF-8'))
                    print(f"[+] {name} Joined")
            except Exception as e:

                self.clients.remove(c)
                print(f"[+] {addr[0]} Left")
                self.sendAll(bytes(f"{len(self.clients)}-",'UTF-8'))
                c.close()
                return
            addr=self.names.get(c.getpeername()[0])
            while True:
                try:
                    msg=c.recv(1024)
                    if(len(msg)==0):
                        continue
                    msg=f"{self.clients.__len__()}-{addr} : {msg.decode()}"
                   
                    self.sendAll(bytes(msg,'UTF-8'),c)
                except:
                   
                    self.clients.remove(c)
                    
                   
                    print(f"[+] {addr} Left")
                    self.sendAll(bytes(f"{len(self.clients)}-",'UTF-8'))
                    c.close()
                    break
                    
   
if __name__=="__main__":
    HOST="IP Address"
    PORT=4444 #Default(If you want to use custom port,change in app.py also)
    Server(HOST,PORT)       


        
        
     
