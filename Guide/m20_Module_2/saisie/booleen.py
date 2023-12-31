"""
Module regroupant toutes les fonctionnalités
permettant de demander une saisie dont la réponse est VRAI/OUI ou FAUX/NON
"""

__all__ = [
    "demander_saisie_oui_ou_non",
    "demander_saisie_vrai_ou_faux",
]


OUI = ("o", "oui", "y", "yes", "1")
VRAI = ("v", "vrai", "t", "true", "1")


def demander_saisie_oui_ou_non(invite):
    """Par défaut, toute réponse non comprise vaut NON"""
    try:
        return input(invite).lower() in OUI
    except ValueError:
        return False


def demander_saisie_vrai_ou_faux(invite):
    """Par défaut, toute réponse non comprise vaut FAUX"""
    try:
        return input(invite).lower() in VRAI
    except ValueError:
        return False
