from tkinter import *
import numpy as np
from scipy import signal
A = np.array([[2,1,3,0],[1,1,0,5],[3,3,1,0],[2,0,0,2]])
M = np.array([[1,0,2],[2,1,0],[1,0,3]])
B = signal.convolve2d(A, M, mode='same', boundary='fill')

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
