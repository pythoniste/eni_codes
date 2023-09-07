"""
Module gérant toutes les fonctionnalités de saisie
"""

from .nombre import (
    demander_saisie_nombre,
    demander_saisie_nombre_borne,
)

from .booleen import (
    demander_saisie_oui_ou_non,
    demander_saisie_vrai_ou_faux,
)

__all__ = [
    "demander_saisie_nombre",
    "demander_saisie_nombre_borne",
    "demander_saisie_oui_ou_non",
    "demander_saisie_vrai_ou_faux",
]
