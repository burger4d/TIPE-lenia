from tkinter import *

tk = Tk()
tk.title("Lenia")
#tk.resizable(False, False)
tk.configure(cursor = "hand2")
w = Canvas(tk,width=640,height=640,bg="#"+str(hex(255))[2:]+str(hex(255)[2:]+str(hex(255))[2:]))
w.pack()
