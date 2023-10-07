import sys
from tkinter import *
import os
import socket,threading
PORT=4444 #Default(If you want to use custom port,change in server.py also)
class App:
    def __init__(this):
        this.window = Tk()
        this.window.title("Chat App")
        this.window.geometry("512x256")
        this.window.configure(bg = "#FFFFFF")
        this.cn=0
        this.index=0
        this.canvas = Canvas(
            this.window,
            bg = "#FFFFFF",
            height = 256,
            width = 512,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        this.canvas.place(x = 0, y = 0)
        this.canvas.create_rectangle(
            0.0,
            0.0,
            512.0,
            256.0,
            fill="#ECFDFF",
            outline="")
        this.canvas.create_text(
            91.0,
            46.0,
            anchor="nw",
            text="Enter address to connect",
            fill="#868686",
            font=("Vollkorn", 24 * -1)
        )
        this.inputBoxImg = PhotoImage(
            file=this.assets("inputBox.png"))
        entry_bg_1 = this.canvas.create_image(
            236.0,
            128.0,
            image=this.inputBoxImg
        )
        this.searchBox = Entry(
            bd=0,
            bg="#FFFFFF",
            highlightthickness=0
        )
        this.searchBox.place(
            x=36.0,
            y=98.0,
            width=405.0,
            height=48.0
        )
        this.i=this.canvas.create_text(
            136.0,
            160,
            anchor="nw",
            text="",
            fill="#868686",
            font=("Vollkorn", 14 * -1)
        )
        this.searchBox.bind("<Return>", this.getResult)

    def getResult(this,event):
        addr=this.searchBox.get()
        this.socketserver = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
        name = socket.gethostname()
        try:
            this.socketserver.connect((addr,PORT))
            this.msgPage()
        except Exception as e:
            this.show_error(this.canvas,this.i,str(e))
    def assets(this,path:str):
        base=os.path.dirname(os.path.abspath(sys.argv[0]))
        return f"{base}\\assets\\{path}"
    def show_error(this,c,i,msg:str,fill="#F10909"):
        return  c.itemconfig(i,
                    text=msg,
                    fill=fill,
                )
    def msgPage(this):
        for item in this.canvas.winfo_children():
            item.destroy()
        this.searchBox.destroy()
        
        this.window.geometry("800x600")
        this.canvas = Canvas(
            this.window,
            bg = "#FFFFFF",
            height = 600,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        this.canvas.place(x = 0, y = 0)
        this.canvas.create_rectangle(
            0.0,
            0.0,
            800.0,
            600.0,
            fill="#7CC7D0",
            outline="")
        this.text=this.canvas.create_text(
            91.0,
            46.0,
            anchor="nw",
            text=f"Connected: {this.cn}",
            fill="#E6FA09",
            font=("Vollkorn", 24 * -1)
        )
        this.chatBoxImg = PhotoImage(
            file=this.assets("chatBox.png"))
        chatBoxEntry = this.canvas.create_image(
            400.0,
            166.0,
            image=this.chatBoxImg
        )
        this.listbox = Listbox(this.window, bd=0,width=45, height=18,highlightthickness=0)
        this.listbox.pack(pady=20)
        iThread = threading.Thread(target=this.recv)
        iThread.daemon = True
        iThread.start()
        this.inputBoxImg = PhotoImage(
            file=this.assets("inputBox.png"))
        entry_bg_1 = this.canvas.create_image(
            416.0,
            378.0,
            image=this.inputBoxImg
        )
        this.searchBox = Entry(
            bd=0,
            bg="#FFFFFF",
            highlightthickness=0
        )
        this.searchBox.place(
            x=216.0,
            y=348.0,
            width=405.0,
            height=48.0
        )
        this.searchBox.bind("<Return>", this.send)
    def recv(this):
        while True:
            data = this.socketserver.recv(1024)
            msg=data.decode().split("-")
            if(int(msg[0])!=this.cn):
                this.cn=int(msg[0])
                this.canvas.itemconfig(this.text,
                    text=f"Connected: {this.cn}",
                )    
            this.listbox.insert(this.index,f"{msg[-1]}\n")
            this.index+=1
            this.canvas.update()
    def send(this,event):
        msg=this.searchBox.get()
        this.socketserver.send(bytes(msg,'UTF-8'))
        this.listbox.insert(this.index,f"You: {msg}\n")
        this.index+=1
        this.searchBox.delete(0, END)

        this.canvas.update()
    def run(this):
        this.window.resizable(False, False)
        this.window.mainloop()
    
    
                
if __name__=="__main__":        
    a=App()
    a.run()                
