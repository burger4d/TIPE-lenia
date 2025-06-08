from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy
import os
import json

tk = Tk()
tk.title("Lenia")
tk.configure(cursor = "hand2")
taille_canevas = 500
w = Canvas(tk,width=taille_canevas,height=taille_canevas,bg="black")
w.pack()

var_ = {"taille":-1}
fichiers = ["Jeudelavie.json", "Primordia.json", "Ltl.json", "Lenia.json"]

def convert_color(n):
    a = str(hex(int(n)))[2:]
    if len(a)==1:
        a="0"+a
    return a


def f_color(x):
    return 255*x, 255*(abs(x-0.5)), 180*(1-x)


def show_mat1(A):
    w.itemconfig("tile", state='hidden')
    unite = int(1+taille_canevas/len(A))
    for i in range(len(A)):
        for j in range(len(A[0])):
            if A[i][j] == 1:
                w.create_rectangle(j*unite, i*unite, (j+1)*unite, (i+1)*unite, fill="white", tag="tile")
    tk.update()


def show_mat2(A, states):
    color_unit = 255//(states-1)
    w.itemconfig("tile", state='hidden')
    unite = int(1+taille_canevas/len(A))
    for i in range(len(A)):
        for j in range(len(A[0])):
            color = str(hex(int(A[i][j])*color_unit))[2:]
            if len(color) == 1:
                color = "0"+color
            w.create_rectangle(j*unite, i*unite, (j+1)*unite, (i+1)*unite, outline="#"+3*color, fill="#"+3*color, tag="tile")
    tk.update()


def show_mat3(A):
    w.itemconfig("tile", state='hidden')
    unite = int(1+taille_canevas/len(A))
    for i in range(len(A)):
        for j in range(len(A[0])):
            r, g, b = list(map(convert_color, f_color(A[i][j])))
            w.create_rectangle(j*unite, i*unite, (j+1)*unite, (i+1)*unite, outline="#"+r+g+b, fill="#"+r+g+b, tag="tile")
    tk.update()


variantes = ["Jeu de la vie", "Primordia", "LtL", "Lenia"]
variante_id = 0


def select_taille():
    global variable, taille, btn2, opt
    taille = echelleTaille.get()
    var_["taille"] = taille
    echelleTaille.destroy()
    btn1.destroy()
    variable = StringVar()
    variable.set(variantes[0])
    opt = OptionMenu(tk, variable, *variantes)
    opt.place(x=200, y=250)
    btn2 = Button(tk, text="choisir la variante", command=select_variante)
    btn2.pack()


def select_variante():
    global KPrimordia, LPrimordia, MPrimordia, NPrimordia, btnChoix0, btnChoix1, variante_id, btnPrimordia, optPrimordia, optLtl, optLtl0, optLtl1, optLtl2, optLtl3, optLtl4, btnLtl, optLenia0, variableLenia, optLenia1, variableLenia2, optLenia, btnLenia, col, couleur
    variante = variable.get()
    for i in range(len(variantes)):
        if variantes[i] == variante:
            variante_id = i
    btn2.destroy()
    opt.destroy()
    couleur = StringVar()
    if variante_id == 1:
        optPrimordia = Scale(tk, orient="horizontal", from_=2, to=50, resolution=1, length=500, label="états:")
        optPrimordia.set(6)
        optPrimordia.place(rely=0.0)
        KPrimordia = Scale(tk, orient="horizontal", from_=0, to=20, resolution=1, length=500, label="K:")
        KPrimordia.set(2)
        KPrimordia.place(rely=0.1)
        LPrimordia = Scale(tk, orient="horizontal", from_=0, to=20, resolution=1, length=500, label="L:")
        LPrimordia.set(0)
        LPrimordia.place(rely=0.2)
        MPrimordia = Scale(tk, orient="horizontal", from_=0, to=20, resolution=1, length=500, label="M:")
        MPrimordia.set(0)
        MPrimordia.place(rely=0.3)
        NPrimordia = Scale(tk, orient="horizontal", from_=0, to=20, resolution=1, length=500, label="N:")
        NPrimordia.set(0)
        NPrimordia.place(rely=0.4)
        col = Checkbutton(tk, text="en couleur", variable=couleur, onvalue="selected", offvalue="not selected")
        couleur.set("not selected")
        col.pack()
        btnPrimordia = Button(tk, text="Sélectionner le nombre d'états", command=lambda:start_Primordia(taille, variante_id))
        btnPrimordia.pack()
    elif variante_id == 2:
        col = Checkbutton(tk, text="en couleur", variable=couleur, onvalue="selected", offvalue="not selected")
        couleur.set("not selected")
        col.pack()
        optLtl = Scale(tk, orient="horizontal", from_=2, to=50, resolution=1, length=500, label="nombre d'états:")
        optLtl.set(2)
        optLtl.place(rely=0.0)
        optLtl0 = Scale(tk, orient="horizontal", from_=1, to=20, resolution=1, length=500, label="rayon:")
        optLtl0.set(5)
        optLtl0.place(rely=0.1)
        optLtl1 = Scale(tk, orient="horizontal", from_=0, to=250, resolution=1, length=500, label="valeur minimale de naissance")
        optLtl1.set(33)
        optLtl1.place(rely=0.2)
        optLtl2 = Scale(tk, orient="horizontal", from_=0, to=250, resolution=1, length=500, label="valeur maximale de naissance")
        optLtl2.set(57)
        optLtl2.place(rely=0.3)
        optLtl3 = Scale(tk, orient="horizontal", from_=0, to=250, resolution=1, length=500, label="valeur minimale de survie")
        optLtl3.set(34)
        optLtl3.place(rely=0.4)
        optLtl4 = Scale(tk, orient="horizontal", from_=0, to=250, resolution=1, length=500, label="valeur maximale de survie")
        optLtl4.set(45)
        optLtl4.place(rely=0.5)
        btnLtl = Button(tk, text="confirmer la sélection de paramètres", command=lambda:start_Ltl(taille, variante_id))
        btnLtl.pack()
        tk.update()
    elif variante_id == 3:
        fonctions =["1 if 0.12<=x<=0.15 else -1"]
        m = [[1 for i in range(11)] for j in range(11)]
        m[5][5] = 0
        noyaux = {"R = 5 (11x11), centre non inclus": m}
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
        noyaux["smooth kernel"] = []
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
        if "Jeudelavie.json" in os.listdir("."):
            btnChoix0 = Button(tk, text="position de départ aléatoire", command=lambda:(deleteChoixPos(),callback(taille, variante_id)))
            btnChoix0.pack()
            btnChoix1 = Button(tk, text="position de départ indiquée manuellement", command=lambda:start_ajoutMotifs(taille, variante_id, aleatoire=False,
                                                                                                                     lancer_=lambda A:callback(taille, variante_id, matrice=A))) 
            btnChoix1.pack()
        else:
            callback(taille, variante_id)#permet de revenir à la fonction lancement() dans main.py


def deleteChoixPos():
    btnChoix0.destroy()
    btnChoix1.destroy()


def start_ajoutMotifs(taille, variante_id, aleatoire, lancer_, etats=2):
    global variablemotif, optmotif, btnAjoutmotif, btnFinmotif, Xmotif, Ymotif, lstmotifs, motifs, matriceinit
    deleteChoixPos()
    if aleatoire:
        callback(taille, variante_id)
    else:
        with open(fichiers[variante_id], "r") as file:
            contenu = file.read()
            contenu = contenu.replace("\n", "")
            motifs = json.loads(contenu)
            file.close()

        lstmotifs = list(motifs.keys())
        variablemotif = StringVar()
        optmotif = OptionMenu(tk, variablemotif, *lstmotifs)
        variablemotif.set(lstmotifs[0])
        optmotif.pack()
        Xmotif = Scale(tk, orient="horizontal", from_=0, to=(taille-1), resolution=1, length=250, label="x (coin supérieur gauche du motif):")
        Xmotif.set(0)
        Xmotif.pack()
        Ymotif = Scale(tk, orient="horizontal", from_=0, to=(taille-1), resolution=1, length=250, label="y (coin supérieur gauche du motif):")
        Ymotif.set(0)
        Ymotif.pack()
        matriceinit = np.zeros((taille, taille))
        btnAjoutmotif = Button(tk, text="ajouter", command=lambda:AjoutMotif(ajout=True, etats=etats))
        btnAjoutmotif.pack()
        btnFinmotif = Button(tk, text="configuration terminée", command=lambda:AjoutMotif(ajout=False, lancer=lancer_, etats=etats))
        btnFinmotif.pack()


def AjoutMotif(ajout, etats=2, lancer=None, lenia=False):
    global matriceinit
    if ajout:
        #on ajoute le motif à la matriceinit
        x = Xmotif.get()
        y = Ymotif.get()
        motif = motifs[variablemotif.get()]
        for i in range(len(motif)):
            for j in range(len(motif[0])):
                matriceinit[(y+i)%taille][(x+j)%taille] = motif[i][j]
        if etats == -1:#Lenia
            show_mat3(matriceinit)
        else:
            show_mat2(matriceinit, etats)
        Xmotif.set(0)
        Ymotif.set(0)
        variablemotif.set(lstmotifs[0])
    else:
        #suppression des derniers boutons,on lance la fonction lancement de main.py avec tout les paramètres
        optmotif.destroy()
        Xmotif.destroy()
        Ymotif.destroy()
        btnAjoutmotif.destroy()
        btnFinmotif.destroy()
        lancer(matriceinit)


def start_Primordia(taille, variante_id):
    global btnChoix0, btnChoix1
    etats = optPrimordia.get()
    K = KPrimordia.get()
    L = LPrimordia.get()
    M = MPrimordia.get()
    N = NPrimordia.get()
    params = [K, L, M, N]
    optPrimordia.destroy()
    btnPrimordia.destroy()
    KPrimordia.destroy()
    LPrimordia.destroy()
    MPrimordia.destroy()
    NPrimordia.destroy()
    c = (couleur.get() == "selected")
    col.destroy()
    if "Primordia.json" in os.listdir("."):
        btnChoix0 = Button(tk, text="position de départ aléatoire", command=lambda:(deleteChoixPos(),callback(taille, variante_id, states=etats, colour=c, primord=params)))
        btnChoix0.pack()
        btnChoix1 = Button(tk, text="position de départ indiquée manuellement", command=lambda:start_ajoutMotifs(taille, variante_id, aleatoire=False, etats=etats, lancer_=lambda A:callback(taille, variante_id, states=etats, colour=c, primord=params, matrice=A)))
        btnChoix1.pack()
        
    else:
        callback(taille, variante_id, states=etats, colour=c)
        

def start_Ltl(taille, variante_id):
    global btnChoix0, btnChoix1
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
    if "Primordia.json" in os.listdir("."):
        btnChoix0 = Button(tk, text="position de départ aléatoire", command=lambda:(deleteChoixPos(),callback(taille, variante_id, R=r, states=etats, ltl_survival=[min(s1, s2), max(s1, s2)], ltl_birth=[min(b1, b2), max(b1, b2)], colour=c)))
        btnChoix0.pack()
        btnChoix1 = Button(tk, text="position de départ indiquée manuellement", command=lambda:start_ajoutMotifs(taille, variante_id, aleatoire=False, etats=etats, lancer_=lambda A:callback(taille, variante_id, R=r, states=etats, ltl_survival=[min(s1, s2), max(s1, s2)], ltl_birth=[min(b1, b2), max(b1, b2)], colour=c, matrice=A)))
        btnChoix1.pack()
        
    else:
        callback(taille, variante_id, R=r, states=etats, ltl_survival=[min(s1, s2), max(s1, s2)], ltl_birth=[min(b1, b2), max(b1, b2)], colour=c)

    
def start_Lenia(taille, variante_id, noyaux):
    global btnChoix0, btnChoix1, kernelR, kernelM, kernelS, kernelBtn
    fonction = variableLenia.get()
    noy = variableLenia2.get()
    kernel = np.array(noyaux[noy])
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
    smooth_k = []
    if noy == "smooth kernel":
        kernelR = Scale(tk, orient="horizontal", from_=1, to=20, resolution=1, length=250, label="R:")
        kernelM = Scale(tk, orient="horizontal", from_=0, to=1, resolution=0.01, length=250, label="m:")
        kernelS = Scale(tk, orient="horizontal", from_=0.01, to=1, resolution=0.01, length=250, label="s:")
        kernelR.set(13)
        kernelM.set(0.5)
        kernelS.set(0.15)
        kernelR.pack()
        kernelM.pack()
        kernelS.pack()
        kernelBtn = Button(tk, text="confirmer paramètres gaussienne f(x)=0.5*exp(-((x-m)/s)^2) pour noyau de rayon R", command=lambda:select_start_pos(taille, variante_id, t, c, fonction, kernel))
        kernelBtn.pack()
    else:
        select_start_pos(taille, variante_id, t, c, fonction, kernel)


def select_start_pos(taille, variante_id, t, c, fonction, kernel):
    global btnChoix0, btnChoix1
    smooth_ker = get_smooth_k()
    print(smooth_ker)
    if "Lenia.json" in os.listdir("."):
        btnChoix0 = Button(tk, text="position de départ aléatoire", command=lambda:(deleteChoixPos(),callback(taille, variante_id, T=t, colour=c, growth=fonction, noyau=kernel, smooth_=smooth_ker)))
        btnChoix0.pack()
        btnChoix1 = Button(tk, text="position de départ indiquée manuellement", command=lambda:start_ajoutMotifs(taille, variante_id, aleatoire=False, etats=-1, lancer_=lambda A:callback(taille, variante_id, T=t, colour=c, growth=fonction, noyau=kernel, matrice=A, smooth_=smooth_ker)))
        btnChoix1.pack()

    else:

        callback(taille, variante_id, T=t, colour=c, growth=fonction, noyau=kernel, smooth_=smooth_ker)

def get_smooth_k():
    print("appel")
    try:
        print("début")
        R = kernelR.get()
        m = kernelM.get()
        s = kernelS.get()
        print("fin-1")
        kernelR.destroy()
        kernelM.destroy()
        kernelS.destroy()
        kernelBtn.destroy()
        print("fin0")
        smooth_k = [R, m, s]
        print("done")
    except Exception as e:
        print(str(e))
        smooth_k = []
    print("sm", smooth_k)
    return smooth_k

def start_ui(callback0):
    global echelleTaille, btn1, callback
    callback = callback0
    echelleTaille = Scale(tk, orient="horizontal", from_=1, to=150, resolution=1, length=250, label="taille de la grille")
    echelleTaille.set(64)
    echelleTaille.pack()
    btn1 = Button(tk, text="confirmer la taille", command=select_taille)
    btn1.pack()
    mainloop()


def click(event):
    taille = var_["taille"]
    if taille != -1:
        unit = 250//taille
        print("x:",event.x*taille//500, "y:", event.y*taille//500)

tk.bind("<Button-3>", click)

def f(x):
    M=3
    N=2
    K=10
    L=6
    if K<=x<=K+L:
        return 1
    elif K-M<=x<=K+L+N:
        return 0
    else:
        return -1
if __name__ == "__main__":
    n=50
    A=[[i for i in range(n+1)] for j in range(n+1)]
    show_mat2(A, states=50)

