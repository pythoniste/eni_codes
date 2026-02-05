#!/usr/bin/python3

import argparse

from pyramid.paster import bootstrap

def show_settings(settings):
    print('Here are settings')
    for k, v in settings.items():
        print('%-40s     %-20s' % (k, v))
    print('Done.')


def get_parser():
    # Étape 1 : définir une fonction proxy vers la fonction principale
    def proxy_show_settings(args):
        """Fonction proxy vers show_settings"""
        try:
            env = bootstrap(args.config_uri)
        except:
            print('Configuration file is not valid: %s' % args.config_uri)
            return
        settings, closer = env['registry'].settings, env['closer']
        try:
            show_settings(settings)
        finally:
            closer()

    # Étape 2 : définir l'analyseur général
    parser = argparse.ArgumentParser(
        prog = 'show_settings',
        description = """Programme permettant de visualiser les paramètres""",
        epilog = """Réalisé pour le livre Python, les fondamentaux du langage"""
    )

    # Rajout des options utiles

    parser.add_argument(
        'config_uri',
        help = """fichier de configuration""",
        type = str,
    )


    # Étape 3 : rajouter le lien entre l'analyseur et la fonction proxy pour calcul_capital
    parser.set_defaults(func=proxy_show_settings)

    return parser




def main():
    parser = get_parser()
    # Étape 4 : démarrer l'analyse des arguments, puis le programme.
    args = parser.parse_args()
    args.func(args)


# Fin du programme

