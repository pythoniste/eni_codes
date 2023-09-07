"""
Exo : Algorithmes deviner_mot
"""


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
    return "todo"


def saisir_mot():
    return demander_saisie_mot("Entrez un mot à deviner: ")


def choisir_de_rejouer():
    return demander_saisie_oui_ou_non(
        "Souhaitez-vous refaire une nouvelle partie ? [o/n]")


def deviner_mot(mot):
    # A ce stade, on sait que mot est composé de lettres minuscules,
    # sans accents, sans espaces, sans tirets.

    lettres_testees = ""
    lettres_trouvees = ""
    # mot_masque = "_" * len(mot)

    while True:
        # Afficher le mot à deviner
        print("Le mot à deviner est '", end="")
        for lettre in mot:
            if lettre in lettres_testees:
                print(lettre, end="")
            else:
                print("_", end="")
        print("'.")

        # On sait que la lettre est aussi minuscule.
        lettre = demander_saisie_lettre("Saisissez une lettre: ")

        if lettre in lettres_testees:
            # On a déjà testé cette lettre, en saisie une autre
            continue
        # On rajoute la nouvelle lettre à la liste de celles que l'on a testé
        lettres_testees += lettre

        # Test de la présence de la lettre
        if lettre in mot:
            lettres_trouvees += lettre
            nb_occurences = mot.count(lettre)
            print("La lettre {} est {} fois dans le mot à trouver".format(
                lettre, nb_occurences))
        else:
            nb_occurences = 0
            print("La lettre {} N'est PAS dans le mot à trouver".format(lettre))

        # Calcul de la position des lettres et affichage dans le mot masqué
        position = -1
        for _ in range(nb_occurences):
            position = mot.find(lettre, position + 1)
            print("La lettre est trouvée à la position {}".format(position))

        # if nb_occurences > 0:
        #     nouveau_mot_masque = ""
        #     for mot_masque_indice, mot_masque_lettre in enumerate(mot_masque):
        #        if mot_masque_indice in positions:
        #             nouveau_mot_masque += lettre
        #         else:
        #             nouveau_mot_masque += mot_masque_lettre
        #     mot_masque = nouveau_mot_masque
        # print("Le mot à deviner est {}".format(mot_masque))

        # As-t-on gagné ?
        # if "_" in liste_lettres_masque:
        #     print("Lettres déjà jouées: {}", ", ".join(lettres_testees))
        # else:
        #     print("Gagné")
        #     return

        # As-t-on gagné ?
        for lettre in mot:
            if lettre not in mot:
                print("Lettres déjà jouées: '{}'.".format(lettres_testees))
                break
        else:
            print("Gagné, le mot était '{}'".format(mot))
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
