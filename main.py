import numpy as np
from scipy import signal
import random
from interface import *

taille = 10

#A=[[random.randint(0,1) for i in range(taille)] for j in range(taille)]
A = [[0 for i in range(taille)] for j in range(taille)]
A[0][1] = 1
A[1][2] = 1
A[2][0] = 1
A[2][1] = 1
A[2][2] = 1
def print_mat(A):
    for i in A:
        print(i)

def update(A):
    B = [[0 for i in range(taille)] for j in range(taille)]
    for i in range(taille):
        for j in range(taille):
            voisins = 0
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if (x, y) != (0, 0):
                        voisins+=A[(i+x+taille)%taille][(j+y+taille)%taille]
            #Une cellule morte possédant exactement trois cellules voisines vivantes devient vivante (elle naît) ;
            #Une cellule vivante ne possédant pas exactement deux ou trois cellules voisines vivantes meurt.
            B[i][j] = A[i][j]
            if i==0 and j==1:
                print(voisins)
            if A[i][j] == 0 and voisins==3:
                B[i][j] = 1
            elif A[i][j] == 1 and (voisins>3 or voisins<2):
                B[i][j] = 0
    return B

while 1:
    print_mat(A)
    show_mat(A)
    input()
    A=update(A)
