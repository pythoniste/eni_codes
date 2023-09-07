#!/usr/bin/python3

import argparse

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from ..models import Subject


def subject(dbSession):
    """Add a contact"""
    for obj in dbSession.query(Subject).all():
        print('> %s' % obj.name)


def get_parser():
    # Étape 1 : définir une fonction proxy vers la fonction principale
    def proxy_subject(args):
        """Fonction proxy vers subject"""
        setup_logging(args.config_uri)
        env = bootstrap(args.config_uri)

        try:
            with env['request'].tm:
                dbsession = env['request'].dbsession
                subject(dbsession)
        except OperationalError:
            print('''
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for description and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.
            ''')

    # Étape 2 : définir l'analyseur général
    parser = argparse.ArgumentParser(
        prog = 'contact',
        description = """Programme permettant de rajouter un Contact""",
        epilog = """Réalisé pour le livre Python, les fondamentaux du langage"""
    )

    # Rajout des options utiles

    parser.add_argument(
        'config_uri',
        help = """fichier de configuration""",
        type = str,
    )

    # Étape 3 : rajouter le lien entre l'analyseur et la fonction proxy pour calcul_capital
    parser.set_defaults(func=proxy_subject)

    return parser


def main():
    parser = get_parser()
    # Étape 4 : démarrer l'analyse des arguments, puis le programme.
    args = parser.parse_args()
    args.func(args)


# Fin du programme

