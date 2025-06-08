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
             "noyau":None,
             "widgets":[],
             "id":None}


def print_mat(A):
    '''affichage de matrice'''
    pprint.pp(list(A))
    print()

def gauss(x, m, s):
        return np.exp(-((x-m)/s)**2 /2)

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
    #l'option "same" indique que la matrice résultante fait la même taille que A.
    #L'option "wrap" signifie que l'on prolonge les cotés de A par les cellules de l'autre coté pour les calculs
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
    K, L, M, N  = variables["primordia_params"]
    if K <= n <= K+L:
        return 1
    elif n < K-M or n > K+L+N:
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
            resultat[i][j] = clip(A[i][j]+delta, 0, primordia_states-1)
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



def smooth_kernel(R, mu, sigma):
    noyau = np.zeros((2*R+1, 2*R+1))
    distance=lambda x,y: np.sqrt((x-R)**2+(y-R)**2)/R
    for i in range(len(noyau)):
        for j in range(len(noyau)):
            d=distance(i, j)
            if 0<d<=1:
                noyau[i][j] = gauss(d, mu, sigma)
    return noyau

def growth4(x):
    """ fonction pour Lenia"""
    return variables["growth"](x) #fonction choisie dans le menu

def update4(A):
    """Lenia"""
    taille = variables["taille"]
    T = variables["T"]

    noyau0 = variables["noyau"]
    noyau = noyau0/np.sum(noyau0)
    resultat = np.zeros_like(A)
    voisinage = scipy.signal.convolve2d(A, noyau, mode='same', boundary='wrap')
    for i in range(taille):
        for j in range(taille):
            #print(i)
            voisins = voisinage[i][j]
            delta = growth4(voisins)
            resultat[i][j] = clip(A[i][j]+(1/T)*delta, 0, 1)
    return resultat



def lancement(taille, variante_id, states=None, R=None, T=None, colour=False, ltl_birth=None, ltl_survival=None, primord=[], growth="1 if 0.12<=x<=0.15 else -1", noyau=None, matrice=None, smooth_ = []):
    '''initialisation des paramètres depuis l'interface graphique'''
    print(smooth_)
    variables["colour"] = colour
    variables["id"] = variante_id
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
        variables["primordia_params"] = primord
        A = np.random.randint(variables["primordia_states"], size=(taille, taille))
        update = update2
        if not variables["colour"]:
            show_mat = lambda x: show_mat2(x, variables["primordia_states"])
        else:
            show_mat = lambda x: show_mat3(x/(variables["primordia_states"]))
    elif variante_id == 2:
        #ltl
        variables["ltl_states"] = states
        A = np.random.randint(variables["ltl_states"], size=(taille, taille))
        update = update3
        if not variables["colour"]:
            show_mat = lambda x: show_mat2(x, (variables["ltl_states"]))
        else:
            show_mat = lambda x: show_mat3(x/(variables["ltl_states"]))
    else:
        #lenia
        variables["noyau"] = noyau
        if len(noyau) == 0:
            print(smooth_)
            R, m, s = smooth_
            variables["noyau"] = smooth_kernel(R, m, s)
        A=np.random.randint(100, size=(taille, taille))
        A=A/100
        update = update4
        if variables["colour"]:
            show_mat = show_mat3
        else:
            show_mat = lambda x: show_mat2((100*x).astype(int), 100)#on convertit les états entre 0 et 1 à des entiers entre 0 et 100
    if matrice is None:
        variables["matrice"] = A
    else:
        variables["matrice"] = matrice
    variables["taille"] = taille
    play=Button(tk, text="Play / Pause", command=lambda: (variables.update({"play": not variables["play"]}), loop(update, show_mat))) #bouton pause
    play.pack()
    enregistreX = Scale(tk, orient="horizontal", from_=0, to=(taille-1), resolution=1, length=250, label="x0:")
    enregistreX.pack()
    enregistreY = Scale(tk, orient="horizontal", from_=0, to=(taille-1), resolution=1, length=250, label="y0:")
    enregistreY.pack()
    enregistreX2 = Scale(tk, orient="horizontal", from_=0, to=(taille-1), resolution=1, length=250, label="x1:")
    enregistreX2.pack()
    enregistreY2 = Scale(tk, orient="horizontal", from_=0, to=(taille-1), resolution=1, length=250, label="y1:")
    enregistreY2.pack()
    enregistreX2.set(taille-1)
    enregistreY2.set(taille-1)
    btnenregistre = Button(tk, text="enregistrer motif entre (x0, y0) et (x1, y1)", command=lambda:enregistrer())
    btnenregistre.pack()
    variables["widgets"] = [enregistreX, enregistreY, enregistreX2, enregistreY2]
    loop(update, show_mat)
    

def enregistrer():
    enregistreX, enregistreY, enregistreX2, enregistreY2 = variables["widgets"]
    taille = variables["taille"]
    x0 = enregistreX.get()
    y0 = enregistreY.get()
    x1 = enregistreX2.get()
    y1 = enregistreY2.get()
    x0, x1 = min(x0, x1), max(x0, x1)
    y0, y1 = min(y0, y1), max(y0, y1)
    mat = variables["matrice"]
    var_id = variables["id"]
    matrix = [[0 for i in range(x1-x0+1)] for j in range(y1-y0+1)]
    for y in range(y1-y0+1):
        for x in range(x1-x0+1):
            if var_id == 3:#lenia
                matrix[y][x] = float(mat[y+y0][x+x0])
            else:
                matrix[y][x] = int(mat[y+y0][x+x0])
    file = fichiers[variables["id"]]
    enregistrements = {}
    if file in os.listdir("."):
        with open(file, "r") as f:
            contenu = f.read()
            contenu = contenu.replace("\n", "")
            enregistrements = json.loads(contenu)
            f.close()
    print(len(matrix))
    enregistrements["nouveau motif ({}, {}), ({}, {})".format(x0, y0, x1, y1)] = matrix
    print(enregistrements)
    with open(file, "w") as f:
        json.dump(enregistrements, f)
        f.close()
    enregistreX.set(0)
    enregistreY.set(0)
    enregistreX2.set(taille-1)
    enregistreY2.set(taille-1)
    

def loop(update, show_mat):
    global energistreX, enregistreY, energistreX2, enregistreY2, btnenregistre
    #print(variables["can_record"])
    if variables["play"]:
        tk.after(2, lambda: iteration(update, show_mat))
    else:#pause
        A = variables["matrice"]
        show_mat(A)
        #print(variables["primordia_params"])


def iteration(update, show_mat):#sinon RecursionError
    A = variables["matrice"]
    show_mat(A)
    variables["matrice"] = update(A)
    loop(update, show_mat)

start_ui(callback0=lancement)
    
