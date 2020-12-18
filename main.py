import argparse
import os
import random

from src import resolv
from src.model.ExportOutput import ExportOutput
from src.model.Grille import Grille
from src.model.ParseInput import ParseInput
from src.model.TypeMap import TypeMap


def required_length(nmin,nmax, sort: bool = False):
    """Fonction donnant le nombre d'arguments min et max

    :param nmin: nombre min d'arguments
    :type: int

    :param nmax: nombre max d'arguments
    :type: int

    :param sort:
    :type: bool
    """
    class RequiredLength(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if not nmin<=len(values)<=nmax:
                msg='argument "{f}" requires between {nmin} and {nmax} arguments'.format(
                    f=self.dest,nmin=nmin,nmax=nmax)
                raise argparse.ArgumentTypeError(msg)
            if len(values) >= 2 and sort:
                assert isinstance(values, list)
                values.sort()
            setattr(args, self.dest, values)
    return RequiredLength


def required_length_in(ns, sort: bool = False):
    class RequiredLength(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if not len(values) in ns:
                msg='argument "{f}" requires in {ns} arguments'.format(
                    f=self.dest, ns=ns)
                raise argparse.ArgumentTypeError(msg)
            if len(values) >= 2 and sort:
                assert isinstance(values, list)
                values.sort()
            setattr(args, self.dest, values)
    return RequiredLength


def param_from_arg(args_dic: dict, param_name: str, nb_value: int, map_chose: TypeMap, type):
    """Retourne une valeur en fonction des arguments donnée du cli et des paramètres par défauts"""
    params = {
        TypeMap.C: {'MAX_STUCK': 10,
                    'MAX_DIST_PM': random.randint (150, 400),
                    'ADDITION': (random.random () * 0.01 + 0.0001,
                                 random.randint (6, 15),
                                 random.randint (6, 15),
                                 random.randint (1, 30)),
                    'FACTEUR_CONCENTRATION_BRAS': 1.25,
                    },
        TypeMap.D: {'MAX_STUCK': 34,
                    'MAX_DIST_PM': 15,
                    'ADDITION': (0.007439079675817982, 6, 15, 2),
                    'FACTEUR_CONCENTRATION_BRAS': 0.99,
                    },
        TypeMap.F: {'MAX_STUCK': 10,
                    'MAX_DIST_PM': random.randint (110, 120),
                    'ADDITION': (0.304678, 13, 5, 42),
                    'FACTEUR_CONCENTRATION_BRAS': 0.1,
                    },
    }
    param = 0

    # set param en fonction des options
    if args_dic[param_name] is not None and len (args_dic[param_name]) > 0:
        if len (args_dic[param_name]) == 1 or (len (args_dic[param_name]) == 2 and nb_value == 1):
            if type == int:
                param = args_dic[param_name][0] if len (args_dic[param_name]) == 1 \
                    else random.randint (args_dic[param_name][0], args_dic[param_name][1])
            else:
                param = args_dic[param_name][0] if len (args_dic[param_name]) == 1 \
                    else random.random()*(args_dic[param_name][1] - args_dic[param_name][0]) + args_dic[param_name][0]

        else:
            param = []
            for i in range(nb_value):
                if type == int:
                    param.append (args_dic[param_name][i] if len (args_dic[param_name]) == nb_value \
                                      else random.randint (args_dic[param_name][i * 2],args_dic[param_name][i * 2 + 1]))
                else:
                    param.append (args_dic[param_name][i] if len (args_dic[param_name]) == nb_value \
                                    else random.random () * (args_dic[param_name][i * 2 + 1] - args_dic[param_name][i * 2]) + \
                                         args_dic[param_name][i * 2])
    else:
        if map_chose in params:
            param = params[map_chose][param_name]
        else:

            raise argparse.ArgumentTypeError (
                f"argument --{param_name} must be given with at less {nb_value} value for map {map_chose.name}")

    return param




if __name__ == "__main__":
    # options choisies
    my_parser = argparse.ArgumentParser (
        description='Retourne des solutions pour le polyhash 2020.'
                    ''
    )

    # toutes les arguments que supporte le cli
    my_parser.add_argument ('-m', '--map',
                            choices=['A', 'B', 'C', 'D', 'E', 'F'],
                            help='choix de la carte',
                            required=True,)

    my_parser.add_argument ('-v', '--verbose',
                            help='active l\'affichage console (temps pour trouver une solution allongé)',
                            action='store_true')

    my_parser.add_argument ('-g', '--graphique',
                            help='active l\'affichage graphique (temps pour trouver une solution énormement allongé)',
                            action='store_true')

    my_parser.add_argument ('-i', '--iteration',
                            help='nombre d\'itération de recherche de solution (defaut = 1)',
                            type=int,
                            default=1)

    my_parser.add_argument ('--MAX_STUCK',
                            help='nombre maximal de fois qu\'un robot peut être bloqué avant une rétractation forcée'
                                 ' (int, si deux valeurs sont données, prend une valeur aléatoire entre les deux)',
                            type=int,
                            nargs='*',
                            action=required_length(0, 2, True))

    my_parser.add_argument ('--MAX_DIST_PM',
                            help='la distance maximal de manhattan de sont point de montage '
                                 'et d\'une tache que peu prendre un robot'
                                 ' (int, si deux valeurs sont données, prend une valeur aléatoire entre les deux)',
                            type=int,
                            nargs='*',
                            action=required_length(0, 2, True))

    my_parser.add_argument ('--ADDITION',
                            help='les quatres facteurs d\'additions lors du choix d\'une tache'
                                 ' (float, si 8 valeurs sont données, prend une valeur aléatoire entre chaque paire)',
                            type=float,
                            nargs='*',
                            action=required_length_in([0, 4, 8], True))

    my_parser.add_argument ('--FACTEUR_CONCENTRATION_BRAS',
                            help='facteur influent sur la distance minimal entre deux robots'
                                 ' lors du choix de leur point de montage'
                                 ' (float, si deux valeurs sont données, prend une valeur aléatoire entre les deux)',
                            type=float,
                            nargs='*',
                            action=required_length(0, 2, True))

    args = my_parser.parse_args ()
    args_dic = vars(args)


    map_chose = TypeMap[args.map]
    iteration = args.iteration
    affichage_graphique = args.graphique
    affichage_console = args.verbose

    FACTEUR_DISTANCE_RETRACTATION = int
    MAX_STUCK = int
    MAX_DIST_PM = int
    ADDITION: tuple
    FACTEUR_CONCENTRATION_BRAS: float

    # récapitulatif de nos options
    print ('Paramètres de la simulation:')
    print ('Map :', map_chose.name)
    print ('Nombre d\'itération :', iteration)
    if affichage_graphique:
        if affichage_console:
            print ('Affichage : graphique et console')
        else:
            print ('Affichage : graphique')
    else:
        if affichage_console:
            print ('Affichage : graphique et console')
        else:
            print ('Affichage : graphique et console')


    grille: Grille = ParseInput().parse(map_chose.get_path())

    best = [None, 0]

    if map_chose == TypeMap.A:
        ExportOutput().exportA()
    else:

        for i in range(iteration):
            MAX_STUCK = param_from_arg(args_dic, 'MAX_STUCK', 1, map_chose, int)
            MAX_DIST_PM = param_from_arg(args_dic, 'MAX_DIST_PM', 1, map_chose, int)
            ADDITION = param_from_arg(args_dic, 'ADDITION', 4, map_chose, float)
            FACTEUR_CONCENTRATION_BRAS = param_from_arg(args_dic, 'FACTEUR_CONCENTRATION_BRAS', 1, map_chose, float)

            # afficher les paramètre de la recherche d'une solution en cours
            print(f'  MAX_STUCK = {MAX_STUCK}')
            print(f'  MAX_DIST_PM = {MAX_DIST_PM}')
            print(f'  ADDITION = {ADDITION}')
            print(f'  FACTEUR_CONCENTRATION_BRAS = {FACTEUR_CONCENTRATION_BRAS}')
            grille_solution = resolv.methode_naive(grille, map_chose, MAX_STUCK, 30, MAX_DIST_PM, ADDITION, FACTEUR_CONCENTRATION_BRAS,
                                                   affichage_graphique=affichage_graphique, affichage_console=affichage_console)
            print(i," points: ", grille_solution.points//1000, " K, ADDITION: ", ADDITION, ", MAX_STUCK: ", MAX_STUCK)

            # Comparaison entre les nouveaux points trouvés et les points de la solution précédente
            if grille_solution.points > best[1]:
                best[1] = grille_solution.points
                best[0] = grille_solution
                print("best_points: ", best[1] if best[1] < 1000 else str(best[1]//1000) + " K")
                ExportOutput().exportOutput(best[0], os.path.basename(map_chose.get_path()) + "_" + str(best[1]) + ".out")
