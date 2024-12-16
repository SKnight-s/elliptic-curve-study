from cherche_courbe import *
from time import time

def hash(mot):
    return sha256(mot.encode()).hexdigest()


def force_brute(P, Q):
    i=1
    P2 = P
    while P2 != Q :
        P2 += P
        i += 1
    return i


def baby_giant_step(P, Q):
    pt = Inf(P.courbe)
    m = math.ceil(math.sqrt(P.courbe.p +1 + 2*math.sqrt(P.courbe.p)))
    table_hachage = {}
    
    for j in range(m+1): 
        table_hachage[hash(str(pt))] = (j,pt)
        pt = pt + P

    P2 = -(m*P)
    Q2 = Q +(-P2)
    for j in range(0, m+1):
        Q2 += P2
        #Q2 = Q + (-(j*m*P)) # moins efficace
        h = hash(str(Q2))
        if h in table_hachage :
            c = table_hachage[h][0]
            return j*m+c

    raise Exception("Pas reussi")


def pollard(P,Q, n):
    """
    Technique du rho de pollard O(sqrt(n)) asymptote pour le temps et O(1) pour l'espace
    Principe : Trouver a1,b1,a2,b2 tel que a1P + b1Q = a2P + b2Q
    pour Q = xP, on a donc x = (a1-a2)*(b2-b1)^-1
    """
    def f(R, a, b): # marche aléatoire
        if R.x < n//3 :
            return R+Q, a, (b+1)%n
        elif R.x > 2*n//3 :
            return R+P, (a+1)%n, b
        else :
            return R+R, (a+a)%n, (b+b)%n

    R1, a1, b1 = f(Q, 0, 1) # R1 = a1P + b1Q
    R2, a2, b2 = f(R1, a1, b1)

    i = 1
    while R1 != R2 and i < 100000 :
        R1, a1, b1 = f(R1, a1, b1)
        R2, a2, b2 = f(R2, a2, b2) # on le fait 2 fois
        R2, a2, b2 = f(R2, a2, b2)
        i += 1

    x = ((a1-a2)*mod_inverse(b2-b1, n))% n # Q = xP
    return x,i


"""
# SONY Attack ------------------------------------
https://github.com/elikaski/ECC_Attacks?tab=readme-ov-file#reusing-the-same-value-of-k-in-different-signatures
h1 = 163716381676276472
h2 = 9826327564862542846
prK = 423332
puK = prK * P
ecdsa = ECDSA(c, P, car)
r1,s1 = ecdsa.sign(h1, prK)
r2,s2 = ecdsa.sign(h2, prK)

def attaque_sony(h1,r1,s1,h2,r2,s2):
    n=car
    assert r1==r2
    k = (h1-h2)*mod_inverse((s1-s2),n) %n 
    return mod_inverse(r1, n)*(s1*k-h1) %n
# ------
"""