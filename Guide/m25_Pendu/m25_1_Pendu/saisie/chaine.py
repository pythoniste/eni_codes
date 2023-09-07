import string
import sys


def demander_saisie_chaine(invite):
    """
    Cette fonction se contente de vérifier que l'on a bien une saisie
    d'au moins un caractère
    """
    while True:
        # On entre dans une boucle infinie

        # On demande la saisie d'un nombre
        saisie = input(invite + ": ")

        if len(saisie) > 0:
            # On a ce que l'on veut, on quitte la boucle en quittant la fonction
            return saisie


def demander_saisie_char(invite):
    """
    Cette fonction se contente de vérifier que l'on a une saisie d'un caractère
    """
    while True:
        # On entre dans une boucle infinie

        # On demande la saisie d'un nombre
        saisie = input(invite + ": ")

        if len(saisie) == 0:
            # On n'a rien saisi
            print("Vous devez saisir au moins un caractère.", file=sys.stderr)
        elif len(saisie) > 1:
            # On n'a rien saisi trop de choses
            print("Vous devez saisir un seul caractère.", file=sys.stderr)
        else:
            # On a ce que l'on veut, on quitte la boucle en quittant la fonction
            return saisie


def demander_saisie_lettre(invite):
    """
    Cette fonction vérifie que l'on a une saisie d'une lettre
    """
    while True:
        # On entre dans une boucle infinie

        saisie = demander_saisie_char(invite)

        if saisie in string.ascii_lowercase:
            # On a ce que l'on veut, on quitte la boucle en quittant la fonction
            return saisie
        elif saisie in string.ascii_uppercase:
            # On a presque ce que l'on veut, on fait en sorte de l'avoir
            return saisie.lower()


def demander_saisie_mot(invite):
    """
    Cette fonction vérifie que l'on a une saisie ne comprennant que des lettres
    """
    while True:
        # On entre dans une boucle infinie

        saisie = demander_saisie_chaine(invite)

        for caractere in saisie:
            if caractere not in string.ascii_letters:
                # Un caractère n'est pas une lettre, on recommence la boucle
                break
        else:
            # Tous les caractères ont été testés et sont des lettres.
            return saisie.lower()


