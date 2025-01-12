import numpy as np
import scipy
import random
import time
from interface import *

taille = 64

#A=[[random.randint(0,1) for i in range(taille)] for j in range(taille)]

#-> glider jeu de la vie
#A = [[0 for i in range(taille)] for j in range(taille)]
'''-> glider jeu de la vie'''
A = np.zeros((taille, taille))
A[0][1] = 1
A[1][2] = 1
A[2][0] = 1
A[2][1] = 1
A[2][2] = 1
"""
np.random.seed(0)
A = np.random.randint(2, size=(taille, taille))
"""
#A = np.random.randint(2, size=(taille, taille))
def print_mat(A):
    '''affichage de matrice'''
    for i in A:
        print(i)


# growth1 et update1 s'appliquent au jeu de la vie que l'on généralise en vue de update2 pour Primordia, puis update3 pour Lenia
def growth1(n, val):
    """ n: nb de voisins entre 0 et 8, val: valeur au centre 0 ou 1"""
    if val == 0 and n==3:
        return 1
    elif val == 1 and (n>3 or n<2):
        return 0
    return val


def update1(A):
    """jeu de la vie -> états discrets, espace continu, temps discret"""

    #B = [[0 for i in range(taille)] for j in range(taille)] #version avec listes

    #--- version avec convolution et A tableau np.array ---
    noyau = np.asarray([[1,1,1],
                        [1,0,1],
                        [1,1,1]]) #noyau permettant de calculer la somme des voisins, donc le nombre de voisins
    V = scipy.signal.convolve2d(A, noyau, mode='same', boundary='wrap') #calcule la somme des voisins pour chaque cellule
    # l'option "same" indique que la matrice résultante fait la même taille que A. L'option "wrap" signifie que l'on prolonge les cotés de A par les cellules de l'autre coté pour les calculs
    B = np.zeros_like(A)
    for i in range(taille):
        for j in range(taille):
            """ --- version avec listes, sans convolution ---
            voisins = 0
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if (x, y) != (0, 0):
                        voisins+=A[(i+x+taille)%taille][(j+y+taille)%taille]
            """
            # Récupération du nombre de voisins vivants pour la cellule (i, j)
            voisins = V[i, j]
            
            #règles:
            #Une cellule morte possédant exactement trois cellules voisines vivantes devient vivante (elle naît)
            #Une cellule vivante ne possédant pas exactement deux ou trois cellules voisines vivantes meurt
            """
            B[i][j] = A[i][j]
            if A[i][j] == 0 and voisins==3:
                B[i][j] = 1
            elif A[i][j] == 1 and (voisins>3 or voisins<2):
                B[i][j] = 0
            """
            B[i][j] = growth1(voisins, A[i][j])

    return B

def growth2(n val):
    """ fonction pour Primordia"""
    """ n: somme des voisins, val: valeur au centre 0 ou 11"""
    #((U>=20)&(U<=24)) - ((U<=18)|(U>=32))
    # Une cellule reste vivante (ou devient vivante) si elle a entre 20 et 24 voisins vivants, inclusivement.
    #Une cellule meurt si elle a 18 voisins vivants ou moins (faible densité) ou 32 voisins vivants ou plus #
    pass

def update2(A):
    """Primordia"""
    pass

def growth3(n val):
    """ fonction pour Lenia"""
    pass

def update3(A):
    """Lenia -> états continus, espace continu, temps continu"""
    pass

while 1:
    #print_mat(A)
    show_mat(A)
    time.sleep(0.1)
    print(1)
    A=update1(A)
