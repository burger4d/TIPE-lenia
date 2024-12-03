from tkinter import *
import numpy as np

'''
tk = Tk()
tk.title("Lenia")
#tk.resizable(False, False)
tk.configure(cursor = "hand2")
w = Canvas(tk,width=640,height=640,bg="#"+str(hex(255))[2:]+str(hex(255)[2:]+str(hex(255))[2:]))
w.pack()
'''

            
def convol(mat, kernel):
    n = len(mat)
    mat2 = [n*[0] for i in range(n)]
    for i in range(len(mat)):
        for j in range(len(mat)):
            acc = 0
            for x in range(len(kernel)):
                for y in range(len(kernel)):
                    if x==i and y==j:
                        acc+=mat[i][j]*kernel[x][y]
            mat2[i][j] = acc
    return mat2
