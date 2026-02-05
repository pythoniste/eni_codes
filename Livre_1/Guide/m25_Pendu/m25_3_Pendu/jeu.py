from random import choice

from saisie import (
    demander_saisie_nombre_borne,
    demander_saisie_oui_ou_non,
    demander_saisie_lettre,
    demander_saisie_mot,
)


def choisir_nombre_joueurs():
    return demander_saisie_nombre_borne(
        "Nombre de joueurs ", 1, 2)


def choisir_mot():
    with open("data/test.txt") as f:
        datas = f.readlines()
    return choice(datas)[:-1]


def saisir_mot():
    return demander_saisie_mot("Entrez un mot à deviner: ")


def choisir_de_rejouer():
    return demander_saisie_oui_ou_non(
        "Souhaitez-vous refaire une nouvelle partie ? [o/n]")


def deviner_mot(mot):
    # A ce stade, on sait que mot est composé de lettres minuscules,
    # sans accents, sans espaces, sans tirets.

    lettres_testees = []
    lettres_trouvees = []
    liste_lettres = list(mot)
    liste_lettres_masque = ["_"] * len(mot)

    while True:
        print("Le mot à deviner est {}".format("".join(liste_lettres_masque)))

        # On sait que la lettre est aussi minuscule.
        lettre = demander_saisie_lettre("Saisissez une lettre: ")

        if lettre in lettres_testees:
            # On a déjà testé cette lettre, en saisie une autre
            continue
        # On rajoute la nouvelle lettre à la liste de celles que l'on a testé
        lettres_testees.append(lettre)

        # Test de la présence de la lettre
        if lettre in liste_lettres:
            lettres_trouvees.append(lettre)
            nb_occurences = liste_lettres.count(lettre)
            print("La lettre {} est {} fois dans le mot à trouver".format(
                lettre, nb_occurences))
        else:
            nb_occurences = 0
            print("La lettre {} N'est PAS dans le mot à trouver".format(lettre))

        # Calcul de la position des lettres et affichage dans le mot masqué
        position = -1
        for _ in range(nb_occurences):
            position = liste_lettres.index(lettre, position + 1)
            liste_lettres_masque[position] = lettre

        # As-t-on gagné ?
        if "_" in liste_lettres_masque:
            print("Lettres déjà jouées: {}", ", ".join(lettres_testees))
        else:
            print("Gagné, le mot à deviner était {}".format("".join(liste_lettres_masque)))
            return


def jouer():
    while True:
        if choisir_nombre_joueurs() == 1:
            mot = choisir_mot()
        else:
            mot = saisir_mot()

        deviner_mot(mot)
        
        if not choisir_de_rejouer():
            return


