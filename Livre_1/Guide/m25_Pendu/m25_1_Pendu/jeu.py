"""
Exercices : écrire demander_saisie_chaine et demander_saisie_caractere
Exercice : écrire choisir_nombre_joueurs, demander_nombre_joueur
"""


from saisie import (
    demander_saisie_nombre_borne,
    demander_saisie_oui_ou_non,
    demander_saisie_lettre,
    demander_saisie_mot,
)


def demander_nombre_joueurs():
    return demander_saisie_nombre_borne(
        "Nombre de joueurs ", 1, 2)


def choisir_mot():
    return "todo"


def demander_saisie_mot_mystere():
    return demander_saisie_mot("Entrez un mot à deviner: ")


def choisir_de_rejouer():
    return demander_saisie_oui_ou_non(
        "Souhaitez-vous refaire une nouvelle partie ? [o/n]")


def deviner_mot(mot):
    # A ce stade, on sait que mot est composé de lettres minuscules,
    # sans accents, sans espaces, sans tirets.

    while True:
        lettre = demander_saisie_lettre("Saisissez une lettre: ")
        # On sait que la lettre est aussi minuscule.

        if lettre in mot:
            print("La lettre {} est dans le mot à trouver".format(lettre))
        else:
            print("La lettre {} N'est PAS dans le mot à trouver".format(lettre))

        break


def jouer():
    while True:
        if demander_nombre_joueurs() == 1:
            mot = choisir_mot()
        else:
            mot = demander_saisie_mot_mystere()

        deviner_mot(mot)
        
        if not choisir_de_rejouer():
            return

