#!/usr/bin/python3

import argparse

from pyramid.paster import bootstrap
from sqlalchemy import engine_from_config
from contact.models import DBSession, Base, Contact, Subject

import transaction

def contact(DBSession, email, subject, text):
    """Add a contact"""
    obj = DBSession.query(Subject).filter_by(name=subject).first()
    if not obj:
        print('Pick a subject in this list:')
        for obj in DBSession.query(Subject).all():
            print('> %s' % obj.name)
        print('Try again.')
        return
    with transaction.manager:
        DBSession.add(Contact(email=email, subject_id=obj.id, text=text))

def get_parser():
    # Étape 1 : définir une fonction proxy vers la fonction principale
    def proxy_contact(args):
        """Fonction proxy vers contact"""
        try:
            env = bootstrap(args.config_uri)
        except:
            print('Configuration file is not valid: %s' % args.config_uri)
            return
        settings, closer = env['registry'].settings, env['closer']
        try:
            engine = engine_from_config(settings, 'sqlalchemy.')
            DBSession.configure(bind=engine)
            Base.metadata.bind = engine
            contact(DBSession, args.email, args.subject, args.text)
        finally:
            closer()

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

    parser.add_argument(
        'email',
        help = """Adresse électronique""",
        type = str,
    )
    parser.add_argument(
        'subject',
        help = """Sujet""",
        type = str,
    )
    parser.add_argument(
        'text',
        help = """Message""",
        type = str,
    )


    # Étape 3 : rajouter le lien entre l'analyseur et la fonction proxy pour calcul_capital
    parser.set_defaults(func=proxy_contact)

    return parser




def main():
    parser = get_parser()
    # Étape 4 : démarrer l'analyse des arguments, puis le programme.
    args = parser.parse_args()
    args.func(args)


# Fin du programme

