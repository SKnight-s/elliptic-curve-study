from matplotlib.pyplot import *
from random import randint
import numpy as np
import math
from hashlib import sha256

def mod_inverse(x, n):
    """
    Effectue l'algorithme d'Euclide augmentée pour trouver l'inverse modulaire
    """
    modulo = n
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n!=0:
        q, x, n = x // n, n, x % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return x0 % modulo

def puissance(a,d,n):
    # calcul p tel que p = a^d mod n
    p=1
    while d > 0:
        if d%2 != 0 :
            p = p*a %n
        a = a*a %n
        d = d//2
    return p

def sqrt(a,p):
    # Resout x^2 = a mod p avec l'algorithme de Tonelli–Shanks
    # 1. Claculer e et n tel que p = 2^e*n + 1
    if puissance(a, (p-1)//2, p) == 1 :
        e=0
        n=p-1
        while True :
            if not n&1 : # si n termine par un 0 (n pair)
                e+=1
                n >>= 1
            else :
                break
        # 2. Trouver u non résidu quadratique mod p
        # si u^k = 1 mod p alors résidu quadratique
        l = 1
        k = (p-1)//2
        while l==1 :
            u = randint(0, p-1)
            l = puissance(u, k, p)

        # 3. Calcul de x
        k = e
        z = puissance(u,n,p)
        x = puissance(a, (n+1)//2,p)
        b = puissance(a,n,p)

        while b != 1 :
            # trouver le plus petit m tel que b^2^m = 1 mod p
            m=0
            r=b
            while r != 1 :
                r = (r*r)% p
                m+=1
            t = puissance(z,puissance(2,k-m-1,p), p)
            z = (t*t)% p
            b = (b*z)% p
            x = (x*t)% p
            k = m
        return x
    else :
        raise Exception("Pas trouve pour " + str(a))

class Courbe_elliptique(object):
    """
    y^2 = x^3 + ax + b mod p
    p nombre premier
    """
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def has_point(self, x, y): # dit si le pt appartient à la courbe
        return (y ** 2) % self.p == (x ** 3 + self.a * x + self.b) % self.p

    def __str__(self):
        return f'y^2 = x^3 + {self.a}x + {self.b} mod {self.p}'

    def afficher(self):
        x = []
        y = []
        for i in range(0,self.p):
            try :
                P1, P2 = self.gen(i)
                x.append(P1.x)
                x.append(P2.x)
                y.append(P1.y)
                y.append(P2.y)
            except :
                pass
        plot(x,y, ".")
        xlim(0, self.p)
        ylim(0, self.p)
        show()

    def gen(self, x) :
        # Génère un point à partir de l'abscisse donné
        x = x % self.p
        y2 = (x ** 3 + self.a * x + self.b) % self.p
        try :
            y = sqrt(y2, self.p)

            return Point(self, x, y), Point(self, x, self.p - y)
        except Exception as e :
            raise e

    def intervalle(self):
        # Donne selon le théorème de Hasse un encadrement du cardinal
        rp = math.ceil(math.sqrt(self.p))
        mini = self.p+1-2*rp
        maxi = self.p+1+2*rp
        return mini, maxi

    def cardinal(self):
        # Calcul le nombre de points appartenant à la courbe elliptique
        mini, maxi = self.intervalle()
        nb = maxi - mini
        possible = []
        i=0
        while i < 20 :
            try :
                P,_ = self.gen(i)

                m = P.order() # m divise N
                if m != 0 and nb//m < 10000 : # Si m est intéressant
                    a = math.ceil(mini/m) # premier entier dans l'intervalle
                    b = math.floor(maxi/m)
                    if possible != [] :
                        possible = intersection(possible, np.arange(a*m,b*m+1,m, dtype=int))
                    else :
                        possible = np.arange(a*m,b*m+1,m, dtype=int)
                    if len(possible)==1:
                        return possible[0]
            except :
                pass
            finally :
                i+=1
        return 4

    def fast_cardinal(self):
        # On veut trouver un cardinal premier
        mini, maxi = self.intervalle()
        i=1
        while i< 20 :
            try :
                P,_ = self.gen(i)
                m = P.order() # m divise N
                if m != 0 :
                    if m > mini and m < maxi :
                        return m
                    else :
                        return 4
            except :
                pass
            finally :
                i+=1
        return 4

class Point(object):
    """
    Definie un point d'une courbe elliptique
    """
    def __init__(self, courbe, x, y):
        self.courbe = courbe
        self.x = x % courbe.p
        self.y = y % courbe.p
        if not isinstance(self, Inf) and not self.courbe.has_point(x, y):
            raise ValueError(f"{self} n\'est pas sur la courbe {self.courbe}")

    def __str__(self):
        if isinstance(self, Inf) :
            return 'Point à l\'infini'
        else :
            return '({}, {})'.format(self.x, self.y)
    """
    def __getitem__(self, index):
        return [self.x, self.y][index]
    """
    def __eq__(self, Q):
        return (self.courbe, self.x, self.y) == (Q.courbe, Q.x, Q.y)

    def __ge__(self,Q):
        if isinstance(Q, Inf) :
            return True
        elif isinstance(self, Inf) :
            return False
        else :
            return  (self.x > Q.x) or (self.x==Q.x and self.y>Q.y)

    def __lt__(self,Q):
        if isinstance(Q, Inf) :
            return False
        elif isinstance(self, Inf) :
            return True
        else :
            return  (self.x < Q.x) or (self.x==Q.x and self.y<Q.y)

    def __neg__(self):
        return Point(self.courbe, self.x, -self.y)
      
    def __add__(self, Q):
        assert self.courbe == Q.courbe # Check si les pts sont sur la meme courbe

        # 0 + P = P
        if isinstance(Q, Inf):
            return self

        xp, yp, xq, yq = self.x, self.y, Q.x, Q.y
        m = None

        # P == Q
        if self == Q:
            if self.y == 0:
                R = Inf(self.courbe)
            else:
                m = ((3 * xp * xp + self.courbe.a) * mod_inverse(2 * yp % self.courbe.p, self.courbe.p)) % self.courbe.p

        # ligne vertical
        elif xp == xq:
            R = Inf(self.courbe)

        # En general
        else:
            m = ((yq - yp) * mod_inverse(xq - xp % self.courbe.p, self.courbe.p)) % self.courbe.p

        if m is not None:
            xr = (m ** 2 - xp - xq) % self.courbe.p
            yr = (m * (xp - xr) - yp) % self.courbe.p
            R = Point(self.courbe, xr, yr)

        return R

    def __mul__(self, n):
        """
        Ne se fait pas en O(n) car sinon cela ne sert à rien
        Se fait en O(log(n)) en decomposant n en base 2
        le problème du log discret repose sur cette difference
        """
        assert isinstance(n, int)

        if n == 0:
            return Inf(self.courbe)
        else:
            Q = self
            R = Inf(self.courbe)
            i = 1
            while i <= n: # Pour optimiser l'addition -> decompose en base 2
                if n & i == i:
                    R = R + Q
                Q = Q + Q
                i = i << 1 # multiplie par 2
        return R

    def __rmul__(self, n):
        return self * n

    def order(self):
        # Algorithme baby-giant step
        Q = Inf(P.courbe)
        pt = Inf(P.courbe)
        m = math.ceil(math.sqrt(P.courbe.p +1 + 2*math.sqrt(P.courbe.p)))
        table_hachage = {}
        for j in range(m+1): 
            table_hachage[hash(str(pt))] = (j,pt)
            pt = pt + P
        for j in range(0, m+1):
            Q2 = Q + (-(j*m*P))
            h = hash(str(Q2))
            if h in table_hachage :
                c = table_hachage[h][0]
                return j*m + c 
        raise Exception("Pas reussi")

class Inf(Point):
    """
    Point infini
    """
    def __init__(self, courbe):
        Point.__init__(self, courbe, 0,0)

    def __eq__(self, Q):
        return isinstance(Q, Inf) 

    def __neg__(self):
        """-0 = 0"""
        return self

    def __add__(self, Q):
        """P + 0 = P"""
        return Q
  
class ECDSA(object):
    def __init__(self, courbe, generator, order):
        self.courbe = courbe
        self.G = generator # point de la courbe choisi
        self.n = order # tel que G.n = 0 (n premier)

    def sign(self, msghash, prK):
        r=0
        s=0
        while r==0 or s==0 :
            k = randint(1, self.n - 1) # on choisit k entre 1 - n-1 (important car si on prend le même ça ne marche plus ex Sony PlayStation 3)
            r = (k * self.G).x # point Q
            s = (mod_inverse(k, self.n) * (msghash + r * prK)) % self.n
        return r, s

    def verify(self, msghash, r, s, puK):
        assert 0<r and r<self.n and 0<s and s<self.n
        w = mod_inverse(s, self.n)
        c = msghash*w %self.n
        d = r*w %self.n
        X = c*self.G + d*puK
        print(r == X.x)