from interface import *
import pprint

np.random.seed(9)

variables = {"matrice":None,
             "taille":None,
             "R":None,
             "primordia_states":None,
             "ltl_states":None,
             "ltl_birth":None,
             "ltl_survival":None,
             "T":None,
             "play":False,
             "colour":False,
             "growth":None,
             "noyau":None}


def print_mat(A):
    '''affichage de matrice'''
    '''
    for i in A:
        print(i)
    print()
    print(A)
    print()
    '''
    pprint.pp(list(A))
    print()


def clip(x, x_min, x_max):
    if x>x_max:
        return x_max
    else:
        return max(x_min, x)


def growth1(n):
    """n: nb de cellules voisines"""
    if n==3:
        return 1
    if n<2 or n>3:
        return -1
    return 0    


def update1(A):
    """jeu de la vie -> états discrets, espace continu, temps discret"""
    taille = variables["taille"]
    noyau = np.asarray([[1,1,1],
                        [1,0,1],
                        [1,1,1]]) #noyau permettant de calculer la somme des voisins, donc le nombre de voisins
    voisinage = scipy.signal.convolve2d(A, noyau, mode='same', boundary='wrap') #calcule la somme des voisins pour chaque cellule
    # l'option "same" indique que la matrice résultante fait la même taille que A. L'option "wrap" signifie que l'on prolonge les cotés de A par les cellules de l'autre coté pour les calculs
    resultat = np.zeros_like(A)
    for i in range(taille):
        for j in range(taille):
            # Récupération du nombre de voisins vivants pour la cellule (i, j)
            voisins = voisinage[i][j]
            
            #règles:
            #Une cellule morte possédant exactement trois cellules voisines vivantes devient vivante (elle naît)
            #Une cellule vivante ne possédant pas exactement deux ou trois cellules voisines vivantes meurt
            delta = growth1(voisins)
            resultat[i][j] = clip(A[i][j]+delta, 0, 1)

    return resultat


def growth2(n):
    """n: somme des voisins"""
    if 20 <= n <= 24:
        return 1
    elif n <= 18 or n >= 32:
        return -1
    else:
        return 0

def update2(A):
    """Primordia"""
    taille = variables["taille"]
    primordia_states = variables["primordia_states"]
    noyau = np.asarray([[1,1,1],
                        [1,0,1],
                        [1,1,1]])
    resultat = np.zeros_like(A)
    voisinage = scipy.signal.convolve2d(A, noyau, mode='same', boundary='wrap')
    for i in range(taille):
        for j in range(taille):
            voisins = voisinage[i][j]
            delta = growth2(voisins)
            resultat[i][j] = clip(A[i][j]+delta, 0, primordia_states)
    return resultat


def growth3(n):
    """ fonction pour LtL"""
    ltl_birth = variables["ltl_birth"]
    ltl_survival = variables["ltl_survival"]
    b1, b2 = ltl_birth
    s1, s2 = ltl_survival
    score = 0
    if b1<=n<=b2:
        score+=1
    if n<s1 or n>s2:
        score-=1
    return score

def update3(A):
    """LtL"""
    taille = variables["taille"]
    R_ltl = variables["R"]
    ltl_states = variables["ltl_states"]
    noyau = np.ones((2*R_ltl+1, 2*R_ltl+1))
    noyau[R_ltl][R_ltl] = 0 #IMPORTANT, ne pas compter le centre
    resultat = np.zeros_like(A)
    voisinage = scipy.signal.convolve2d(A, noyau, mode='same', boundary='wrap')
    for i in range(taille):
        for j in range(taille):
            voisins = voisinage[i][j]
            delta = growth3(voisins)
            resultat[i][j] = clip(A[i][j]+delta, 0, ltl_states-1)
    return resultat


def growth4(x):
    """ fonction pour Lenia"""
    '''
    #print(n)
    if 0.12<=x<=0.15:
        return 1
    return -1
    '''
    #print(variables["growth"])
    return variables["growth"](x)

def update4(A):
    """Lenia -> états continus, espace continu, temps continu"""
    taille = variables["taille"]
    R_lenia = 5
    T = variables["T"]
    #noyau = np.full((2*R_lenia+1, 2*R_lenia+1), 1)#/((2*R_lenia+1)**2 - 1))
    #noyau[R_lenia][R_lenia] = 0
    #print(noyau[0][0], variables["noyau"][0][0], noyau[0][0] == variables["noyau"][0][0])
    noyau0 = variables["noyau"]
    noyau = noyau0/np.sum(noyau0)
    #print_mat(noyau)
    """
    for i in range(len(noyau)):
        for j in range(len(noyau)):
            if j == 0:
                print("[", end="")
            print(noyau[i][j], end="")
            if j == len(noyau)-1:
                print("],")
            else:
                print(",", end=" ")
    quit()
    """
    resultat = np.zeros_like(A)
    voisinage = scipy.signal.convolve2d(A, noyau, mode='same', boundary='wrap')
    for i in range(taille):
        for j in range(taille):
            #print(i)
            voisins = voisinage[i][j]
            delta = growth4(voisins)
            resultat[i][j] = clip(A[i][j]+(1/T)*delta, 0, 1)
    return resultat
'''
while 1:
    #print_mat(A)
    #show_mat2(A, ltl_states-1)
    show_mat3(A)
    #input()
    #time.sleep(1)
    A=update4(A)
    #print(1)
    #A=update2(A)
'''


def lancement(taille, variante_id, states=None, R=None, T=None, colour=False, ltl_birth=None, ltl_survival=None, growth="1 if 0.12<=x<=0.15 else -1", noyau=None):
    '''initialisation des paramètres depuis l'interface graphique'''
    variables["colour"] = colour
    #variables["growth"] = growth
    variables["R"] = R
    variables["T"]=T
    variables["ltl_survival"] = ltl_survival
    variables["ltl_birth"] = ltl_birth
    s='variables["growth"] = lambda x: '+growth
    exec(s)
    if variante_id == 0:
        #jeu de la vie
        A = np.random.randint(2, size=(taille, taille))
        update = update1
        show_mat = show_mat1
    elif variante_id == 1:
        #primordia
        variables["primordia_states"] = states
        A = np.random.randint(variables["primordia_states"], size=(taille, taille))
        update = update2
        if not variables["colour"]:
            print(variables["colour"])
            show_mat = lambda x: show_mat2(x, variables["primordia_states"])
        else:
            print(variables["colour"])
            show_mat = lambda x: show_mat3(x/(variables["primordia_states"]))
    elif variante_id == 2:
        #ltl
        variables["ltl_states"] = states
        A = np.random.randint(variables["ltl_states"], size=(taille, taille))
        update = update3
        if not variables["colour"]:
            show_mat = lambda x: show_mat2(x, (variables["ltl_states"]-1))
        else:
            show_mat = lambda x: show_mat3(x/(variables["ltl_states"]-1))
    else:
        #lenia
        #variables["R"] = 5
        variables["noyau"] = noyau
        A=np.random.randint(100, size=(taille, taille))
        A=A/100
        update = update4
        if variables["colour"]:
            show_mat = show_mat3
        else:
            show_mat = lambda x: show_mat2((100*x).astype(int), 10)#on convertit les états entre 0 et 1 à des entiers entre 0 et 100
    variables["matrice"] = A
    variables["taille"] = taille
    play=Button(tk, text="Play / Pause", command=lambda: (variables.update({"play": not variables["play"]}),loop(update, show_mat))) #bouton pause
    play.pack()
    loop(update, show_mat)
    


def loop(update, show_mat):
    if variables["play"]:
        tk.after(10, lambda: iteration(update, show_mat))
    else:
        A = variables["matrice"]
        show_mat(A)


def iteration(update, show_mat):
    A = variables["matrice"]
    show_mat(A)
    variables["matrice"] = update(A)
    loop(update, show_mat)

start_ui(callback0=lancement)
