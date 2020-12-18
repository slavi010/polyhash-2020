# PolyHash 2020
============

Pour ce projet, nous avons cherché à résoudre le problème posé lors du Google hash code de 2020.

# Notre équipe
===========
* Sviatoslav BESNARD
* Aurelie BOULAIS
* Chama EL MAJENY
* Remy BORIUS

# Quick start
Pour lancer une recherche de solution sur la carte A (ou fichier d'input A) lancez :
```bash
python main.py -m A
```
Il y a 6 carte de A à F.

Seules les cartes C, D et F ont déjà des paramètres de simulation par défaut pour la recherche de solution.
La carte A n'a pas besoin de paramètres de simulation, car sa recherche de solution est statique.

Un fichier à la racine sera créé avec le nom de la carte.

Pour toutes questions, vous pouvez afficher l'aide :
```bash
python main.py -h
```

## Paramètres de simulation
Pour trouver une solution aux cartes B ou E ou si vous souhaitez modifier manuellement les paramètres de simulation, vous devez modifier les arguments : ```MAX_STUCK```, ```MAX_DIST_PM```, ```ADDITION``` et ```FACTEUR_CONCENTRATION_BRAS```.

Exemple : 
```bash
python main.py -m F --MAX_STUCK 10 --MAX_DIST_PM 115 --ADDITION 0.304678 13 5 42 --FACTEUR_CONCENTRATION_BRAS 0.1
```
```MAX_STUCK```, ```MAX_DIST_PM``` ne prennent qu'une seule valeur de type entier.
```ADDITION``` prendre quatre valeurs de type float et ```FACTEUR_CONCENTRATION_BRAS``` en prend une de type float.

Il est possible pour ces paramètres de choisir une valeur aléatoire dans une intervalle.
```bash
python main.py -m F --MAX_STUCK 10 20
```
Ici ```MAX_STUCK``` prendra une valeur aléatoire entre 10 et 20 avec une distribution uniforme.

## Itération
L'option ```--iteration``` (ou ```-i```) permet de spécifier au programme le nombre de fois qu'il doit exécuter la recherche de solution. Chaque solution trouvée sera enregistrée dans un fichier avec son score correspondant. Il est préférable d'utiliser cette option en conjonction de spécifier aux paramètres de la simulation des valeurs dans un intervale.

## Affichage
### Console
L'option ```--verbose``` (ou ```-v```) permet d'afficher plus de détail dans la console. Notamment un pourcentage d'avancement de la recherche de solution en cours.
### Graphique
Pour afficher l'interface graphique qui affiche la recherche de solution en temps réel, il faut utiliser l'option ```--graphique``` (ou ```-g```).
Attention ! L'affichage de cette interface va diminuer de manière drastique la vitesse d'exécution.

![Image de l'interface graphique](https://uncloud.univ-nantes.fr/index.php/s/NJrBcn5TdfjrzkP/preview)

