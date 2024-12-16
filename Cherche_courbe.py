from cypari import *
from Classe_courbe import *

def calcul_premier(n):
    # crible d'eratosthène
    # max pour n : 20 000
    def supprime(i,tab):
        for j in tab :
            if j > i and j % i == 0 :
                tab.remove(j)

    maxi = math.sqrt(n) 
    crible = [i for i in range(2,n)]
    for i in crible:
        if i < maxi :
            supprime(i,crible)
    return crible

def rabin(n,k):
    # Test de primalité probabiliste (échec : 4**(-k))
    #https://fr.wikipedia.org/wiki/Test_de_primalit%C3%A9_de_Miller-Rabin#:~:text=Le%20th%C3%A9or%C3%A8me%20de%20Rabin%20permet,est%20inf%C3%A9rieure%20%C3%A0%204%E2%88%92k.
    # calcul de s et d tel que n-1 = 2**s *d
    s=0
    d=n-1
    while True :
        if not d&1 : # si d termine par un 0 (d pair)
            s+=1
            d >>= 1
        else :
            break

    def temoin_miller(n,a):
        x = puissance(a,d,n)
        if x==1 or x==n-1 :
            return False
        
        for i in range(s):
            x = x*x % n
            if x == n-1 :
                return False
        return True

    for i in range(k): # On effectue k fois le test de miller
        a = randint(2, n-2)
        if temoin_miller(n, a) :
            return False
    return True

def card(c, methode):
    if methode == 1 :
        pari('E = ellinit(['+str(c.a)+','+str(c.b)+'],{D='+str(c.p)+'})')
        return int(pari('ellcard(E)'))
    else :
        return c.fast_cardinal()

def random_curve(p):
    """
    On devrait prendre un seed et déduire du hash a et b
    Nothing-up-my-sleeve number
    """
    found = False
    while not found :
	    a = randint(0,p-1)
	    b = randint(0, p-1)
	    if 4*int((a**3)) + 27*int((b**2)) :
	        return Courbe_elliptique(a, b, p)

def search_curve(p, maxi):
    i=0
    while i<maxi :
        c = random_curve(p)
        N = card(c,1)
        if N%2 and rabin(N, 3): # Si N est premier
            j=0
            while j<50 :
                try :
                    P,_ = c.gen(j)
                    print("Courbe "+str(c)+ " de cardinal "+str(N)+" trouvée"+" Point generateur : "+str(P))
                    return c,P,N
                except :
                    j+=1
            break
        i+=1
    raise Exception("pas trouve")

