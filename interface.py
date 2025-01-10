from tkinter import *

tk = Tk()
tk.title("Lenia")
#tk.resizable(False, False)
tk.configure(cursor = "hand2")
taille_canevas = 500
w = Canvas(tk,width=taille_canevas,height=taille_canevas,bg="white")
w.pack()

def show_mat(A):
    w.itemconfig("tile", state='hidden')
    unite = int(taille_canevas//len(A))
    for i in range(len(A)):
        for j in range(len(A[0])):
            if A[i][j] == 1:
                w.create_rectangle(j*unite, i*unite, (j+1)*unite, (i+1)*unite, fill="black", tag="tile")
    tk.update()
