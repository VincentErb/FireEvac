Aussi disponible dans le rapport.
# Input_reader
## parse_instance
Fonction qui prend pour argument le chemin vers un fichier de données et renvoie deux dictionnaires de données evac_path et arcs.

Afin de "parser" le fichier et de remplir les dictionnaires, la fonction lit les lignes une à une et mots par mots. Ainsi comme les fichiers de données ont une strucutre bien spécifique on sait suivant le placement de chaque mot où le placer dans le dictionnaire. Pour le dictionnaire evac_path nous attribuons à chaque noeud de départ (keys) les valeurs suivantes (values) : pop, max_rate, route_length et route_nodes. Pour le dictionnaire arcs nous attribuons à chaque tuple de noeud (keys) les valeurs suivantes (values) : duedate, length et capacity.
## parse_solution 
Fonction qui prend pour argument un chemin vers un fichier solution et qui renvoie un dictionnaire solution.
## print_input_data
Fonction qui prend pour arguments un dictionnaire de type evac_path et un de type arcs et les print sur le terminal à l'aide d'une boucle for.

Le parser de solution fonctionne de manière similaire à celui qui parse les instances. Pour le dictionnaire solution nous attribuons à chaque node_data (keys) les valeurs suivantes (values) : instance_name, nb_evac_nodes, validity, aim_function, time et method. node_data est un tuple composé de : id (de départ), evac_rate et start.

# Checker
## run
Fonction qui prend pour argument un chemin vers un fichier instance ET un fichier solution et qui renvoie un affichage textuel de vérification de la validité de la solution.
## run_dico
Fonction qui prend pour argument un chemin vers un fichier instance et un dicitonnaire solution et qui renvoie un affichage textuel de vérification de la validité de la solution.
## run_with_objective
Fonction qui prend pour argument un chemin vers un fichier instance et un dictionnaire solution et qui renvoie un tuple booléen/entier : (valide, fonction_objectif).
## run_with_objective_parsed
Fonction qui prend pour argument un dictionnaire d'instance déjà parsée et un dictionnaire solution et qui renvoie un tuple booléen/entier : (valide, fonction_objectif).

# Bornes
## borne_inf 
Fonction qui prend pour arguments un dictionnaire evac_path et  un arcs, elle retourne la valeur objectif de temps d'évacuation.

L'algorithme parcours les chemins d'évacuations afin de faire la somme de la taille de chaque arcs pour obtenir la taille totale de chaque chemin d'évacuation. Ensuite pour chacun des chemin on additione ce trajet total et le resultat de la division du nombre de personnes à évacuer par le débit max d'évacuation. On obtient ainsi la durée d'évacuation d'un chemin d'évacuation. La fonction retourne le plus long de ces durées, c'est-à-dire le temps d'évacuation totale de tout les noeuds avec une évacuation simultanée.
## borne_sup
Fonction qui prend pour arguments un dictionnaire evac_path et  un arcs, elle retourne une heurisique du temps d'évacuation.

L'algorithme parcours les chemins d'évacuations afin de faire la somme de la taille de chaque arcs pour obtenir la taille totale de chaque chemin d'évacuation. Ensuite pour chacun des chemins on additione ce trajet total et le résultat de la division du nombre de personnes à évacuer par le débit max d'évacuation. On obtient ainsi la durée d'évacuation d'un chemin d'évacuation. La fonction retourne la somme de ces durées, c'est-à-dire le temps d'évacuation totale de tout les noeuds avec des évacuations consécutives.
## borne_sup_solution
Fonction qui prend pour arguments un dictionnaire evac_path et un arcs, elle retourne un dictionnaire solution.

L'algorithme fonctionne comme celui de borne_sup sauf que nous mémorisons certaines valeurs au cours de sa réalisation afin de remplir ensuite le dictionnaire à retourner.


# Local_search
## local_search 
Fonction qui prend en entrée un chemin d'instance, un dictionnaire evac_path, un dictionnaire arc et un dictionnaire solution et retourne un autre dictionnaire solution.

La partie instensification  se fait par le tirage au sort de deux nombres aléatoires : un pour le chemin a modifier et un pour la modification à effectuer. On appelle ensuite la fonction modify_solution qui prend en entrée ces nombres aléatoires et nous renvoit la solution modifée.

On teste si la nouvelle solution est mieux que la meilleure solution à ce jour, si c'est le cas on la remplace. On ré-itère avec cette meilleure solution (qui a changée ou est restée la même).

La recherche s'arrête si on égalise la fonction objectif (même si on arrive à la meilleur solution et qu'elle est différente de la fonction objectif on ne s'arrête pas) ou si on atteint le nombre d'itérations maximum.

L'implémentation de la diversification c'est faite par la mise en place d'un compteur et le rajout de deux conditions if qui permettent de traiter le cas où la solution est fausse et le cas où la solution est fausse et le compteur à atteint son maximum.

On enregistre dans deux tableaux la meilleure solution vraie et la meilleure solution fausse afin de pouvoir retourner à la dernière meilleure solution vraie en cas de dépassement du comtperu lors de l'exploration de solutions fausses.

## modify_solution
Fonction  qui prend en entrée un dictionnaire solution, un entier correspondant à un chemin à modifier et un entier correspondant à une modifiction.

Au départ de la fonction on fait une copie profonde du dictionnaire, ce qui est essentiel vu que notre dictionnaire contient un autre dictionnaire. En effet, si on faisait une simple copie, les deux copies du dictionnaires solution contiendrait le même dictionnaire node_data.

L'entier du chemin à modifier correspond au numéro de départ du chemin qui est la clé du dictionnaire node_data qui est lui même une clé du dictionnaire solution.

L'entier pour les modifications entraîne 4 modifications possible : +1 ou -1 sur le temps de départ / +1 ou -1 sur la taille du convoi.

On renvoit la nouvelle solution.
