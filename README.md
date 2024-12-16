# Elliptic Curve Study

Pour mon TIPE en 2021, j'ai étudié le fonctionnement des courbes elliptiques et leur utilisation dasn la blockchain.
Une blockcahin locale a été implémenté mais n'est pas facilement utilisable.

Mes travaux peuvent être séparés en plusieurs parties :

### Recherche de nombres premiers
Il existe plusieurs critères pour choisir une courbe elliptique pour la cryptographie.
Un d'entre eux est de réussir à obtenir un grand nombre premier. Y arriver avec déterminisme est impossible ; on utilise plutôt des algorithmes probabilistes qui vérifient qu'un nombre est premier (avec une certaine probabilité).

Voir [Cherche_courbe.py](./Cherche_courbe.py)

### Implémentation de ECDSA
Les points sur la courbe elliptique ainsi que les opérations entre eux sont implémentées. Cela sert ensuite pour les fonctions de signatures et vérifications de ECDSA.

Voir [Classe_courbe.py](./Classe_courbe.py)

### Attaque contre ECSA et les courbes elliptiques
Etude et comparaison de différents scénarios d'attaque contre la signature ECDSA.
La force vrute, la technique du baby-step giant-step ainsi que le rho de Pollard sont utilisées.

Voir [Classe_attaque.py](./Classe_attaque.py)
