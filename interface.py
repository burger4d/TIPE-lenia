from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy
import os
import json

tk = Tk()
tk.title("Lenia")
#tk.resizable(False, False)
tk.configure(cursor = "hand2")
taille_canevas = 500
w = Canvas(tk,width=taille_canevas,height=taille_canevas,bg="black")
w.pack()


def convert_color(n):
    a = str(hex(int(n)))[2:]
    if len(a)==1:
        a="0"+a
    return a


def f_color(x):
    #"""
    return 255*x, 255*(abs(x-0.5)), 180*(1-x)
    #"""
    #return 255*x, 255*x, 255*x


def show_mat1(A):
    #print("1")
    w.itemconfig("tile", state='hidden')
    unite = int(1+taille_canevas/len(A))
    for i in range(len(A)):
        for j in range(len(A[0])):
            if A[i][j] == 1:
                w.create_rectangle(j*unite, i*unite, (j+1)*unite, (i+1)*unite, fill="white", tag="tile")
    tk.update()


def show_mat2(A, states):
    color_unit = 255//states
    w.itemconfig("tile", state='hidden')
    unite = int(1+taille_canevas/len(A))
    for i in range(len(A)):
        for j in range(len(A[0])):
            color = str(hex(int(A[i][j])*color_unit))[2:]
            if len(color) == 1:
                color = "0"+color
            w.create_rectangle(j*unite, i*unite, (j+1)*unite, (i+1)*unite, fill="#"+3*color, tag="tile")
    tk.update()


def show_mat3(A):
    w.itemconfig("tile", state='hidden')
    unite = int(1+taille_canevas/len(A))
    for i in range(len(A)):
        for j in range(len(A[0])):
            r, g, b = list(map(convert_color, f_color(A[i][j])))
            #print(r, g, b)
            w.create_rectangle(j*unite, i*unite, (j+1)*unite, (i+1)*unite, fill="#"+r+g+b, tag="tile")
    tk.update()

#A=[[i/12 for i in range(13)] for j in range(12)]

#show_mat3(A)
variantes = ["Jeu de la vie", "Primordia", "LtL", "Lenia"]
variante_id = 0


def select_taille():
    global variable, taille, btn2, opt
    taille = echelleTaille.get()
    echelleTaille.destroy()
    btn1.destroy()
    variable = StringVar()
    variable.set(variantes[0])
    opt = OptionMenu(tk, variable, *variantes)
    opt.place(x=200, y=250)
    btn2 = Button(tk, text="choisir la variante", command=select_variante)
    btn2.pack()


def select_variante():
    global variante_id, btnPrimordia, optPrimordia, optLtl, optLtl0, optLtl1, optLtl2, optLtl3, optLtl4, btnLtl, optLenia0, variableLenia, optLenia1, variableLenia2, optLenia, btnLenia, col, couleur
    variante = variable.get()
    for i in range(len(variantes)):
        if variantes[i] == variante:
            variante_id = i
    btn2.destroy()
    opt.destroy()
    couleur = StringVar()
    if variante_id == 1:
        optPrimordia = Scale(tk, orient="horizontal", from_=2, to=50, resolution=1, length=250, label="états:")
        optPrimordia.set(12)
        optPrimordia.pack()
        col = Checkbutton(tk, text="en couleur", variable=couleur, onvalue="selected", offvalue="not selected")
        couleur.set("not selected")
        col.pack()
        btnPrimordia = Button(tk, text="Sélectionner le nombre d'états", command=lambda:start_Primordia(taille, variante_id))
        btnPrimordia.pack()
    elif variante_id == 2:
        col = Checkbutton(tk, text="en couleur", variable=couleur, onvalue="selected", offvalue="not selected")
        couleur.set("not selected")
        col.pack()
        optLtl = Scale(tk, orient="horizontal", from_=2, to=50, resolution=1, length=250, label="nombre d'états:")
        optLtl.set(2)
        optLtl.place(rely=0.0)
        optLtl0 = Scale(tk, orient="horizontal", from_=1, to=20, resolution=1, length=250, label="rayon:")
        optLtl0.set(5)
        optLtl0.place(rely=0.1)
        optLtl1 = Scale(tk, orient="horizontal", from_=0, to=60, resolution=1, length=250, label="valeur minimale de naissance")
        optLtl1.set(33)
        optLtl1.place(rely=0.2)
        optLtl2 = Scale(tk, orient="horizontal", from_=0, to=60, resolution=1, length=250, label="valeur maximale de naissance")
        optLtl2.set(57)
        optLtl2.place(rely=0.3)
        optLtl3 = Scale(tk, orient="horizontal", from_=0, to=60, resolution=1, length=250, label="valeur minimale de survie")
        optLtl3.set(34)
        optLtl3.place(rely=0.4)
        optLtl4 = Scale(tk, orient="horizontal", from_=0, to=60, resolution=1, length=250, label="valeur maximale de survie")
        optLtl4.set(45)
        optLtl4.place(rely=0.5)
        btnLtl = Button(tk, text="confirmer la sélection de paramètres", command=lambda:start_Ltl(taille, variante_id))
        btnLtl.pack()
        tk.update()
    elif variante_id == 3:
        fonctions =["1 if 0.12<=x<=0.15 else -1"]
        noyaux = {"R = 5 (11x11), centre non inclus":
[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]}
        if "fonctions.txt" in os.listdir("."):
            with open("fonctions.txt", "r") as file:
                contenu = file.read()
                fonctions = contenu.split("\n")
                file.close()
        if "kernel.json" in os.listdir("."):
            with open("kernel.json", "r") as file:
                contenu = file.read()
                contenu2 = contenu.replace("\n", "")
                noyaux = json.loads(contenu2)
                file.close()
        noy = list(noyaux.keys())
        
        variableLenia = StringVar()
        variableLenia.set(fonctions[0])
        optLenia0 = OptionMenu(tk, variableLenia, *fonctions)
        optLenia0.place(x=200, y=250)
        variableLenia2 = StringVar()
        variableLenia2.set(noy[0])
        optLenia1 = OptionMenu(tk, variableLenia2, *noy)
        optLenia1.place(x=200, y=350)
        col = Checkbutton(tk, text="en couleur", variable=couleur, onvalue="selected", offvalue="not selected")
        couleur.set("selected")
        col.pack()
        optLenia = Scale(tk, orient="horizontal", from_=1, to=30, resolution=1, length=250, label="fraction de temps:")
        optLenia.set(10)
        optLenia.pack()
        btnLenia = Button(tk, text="confirmer la fonction de croissance", command=lambda:start_Lenia(taille, variante_id, noyaux))
        btnLenia.pack()
    else:
        callback(taille, variante_id)#permet de revenir à la fonction lancement() dans main.py


def start_Primordia(taille, variante_id):
    etats = optPrimordia.get()
    optPrimordia.destroy()
    btnPrimordia.destroy()
    c = (couleur.get() == "selected")
    col.destroy()
    callback(taille, variante_id, states=etats, colour=c)


def start_Ltl(taille, variante_id):
    etats = optLtl.get()
    r = optLtl0.get()
    b1 = optLtl1.get()
    b2 = optLtl2.get()
    s1 = optLtl3.get()
    s2 = optLtl4.get()
    optLtl.destroy()
    optLtl0.destroy()
    optLtl1.destroy()
    optLtl2.destroy()
    optLtl3.destroy()
    optLtl4.destroy()
    btnLtl.destroy()
    c = couleur.get() == "selected"
    col.destroy()
    callback(taille, variante_id, R=r, states=etats, ltl_survival=[min(s1, s2), max(s1, s2)], ltl_birth=[min(b1, b2), max(b1, b2)], colour=c)

    
def start_Lenia(taille, variante_id, noyaux):
    fonction = variableLenia.get()
    kernel = np.array(noyaux[variableLenia2.get()])
    #print(kernel, type(kernel[0]))
    optLenia0.destroy()
    t = optLenia.get()
    optLenia.destroy()
    optLenia1.destroy()
    btnLenia.destroy()
    c = couleur.get() == "selected"
    col.destroy()
    x = np.linspace(0, 1, 400)
    f = lambda x: eval(fonction)
    f_vect = np.vectorize(f)#on rend la fonction compatible avec les np.arrays
    y = f_vect(x)
    
    plt.plot(x, y)
    plt.title("f(x) = "+fonction)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.show(block=False)
    callback(taille, variante_id, T=t, colour=c, growth=fonction, noyau=kernel)
    

def start_ui(callback0):
    global echelleTaille, btn1, callback
    callback = callback0
    echelleTaille = Scale(tk, orient="horizontal", from_=1, to=80, resolution=1, length=250, label="taille de la grille")
    echelleTaille.set(64)
    echelleTaille.pack()
    btn1 = Button(tk, text="confirmer la taille", command=select_taille)
    btn1.pack()
    mainloop()
