"""Moteur de calcul de la calculatrice.

Ce module contient uniquement la logique métier, sans aucune dépendance
à l'interface graphique. Il est donc testable de façon unitaire et pourra
être réutilisé si l'IHM évolue (autre framework, ajout d'un mode CLI, etc.).
"""

from __future__ import annotations

from enum import Enum


class Operation(Enum):
    """Les quatre opérations supportées."""

    ADDITION = "+"
    SOUSTRACTION = "-"
    MULTIPLICATION = "×"
    DIVISION = "÷"


class ErreurDivisionParZero(Exception):
    """Levée lorsqu'une division par zéro est tentée."""


def calculer(operande_gauche: float, operation: Operation, operande_droit: float) -> float:
    """Applique l'opération demandée aux deux opérandes.

    Args:
        operande_gauche: premier nombre.
        operation: opération à appliquer.
        operande_droit: second nombre.

    Returns:
        Le résultat du calcul.

    Raises:
        ErreurDivisionParZero: si operation est DIVISION et operande_droit vaut 0.
    """
    if operation is Operation.ADDITION:
        return operande_gauche + operande_droit
    if operation is Operation.SOUSTRACTION:
        return operande_gauche - operande_droit
    if operation is Operation.MULTIPLICATION:
        return operande_gauche * operande_droit
    if operation is Operation.DIVISION:
        if operande_droit == 0:
            raise ErreurDivisionParZero("Division par zéro impossible.")
        return operande_gauche / operande_droit
    raise ValueError(f"Opération inconnue : {operation}")


class MachineCalculatrice:
    """Machine à états portant la logique d'une calculatrice à affichage unique.

    Reproduit le comportement classique d'une calculatrice physique :
    saisie d'un nombre, choix d'une opération, saisie du second nombre,
    calcul du résultat sur "=".
    """

    def __init__(self) -> None:
        self._reinitialiser_etat()

    def _reinitialiser_etat(self) -> None:
        self.affichage: str = "0"
        self._operande_en_attente: float | None = None
        self._operation_en_attente: Operation | None = None
        self._saisie_en_cours_de_nombre: bool = True
        self._resultat_venant_d_etre_calcule: bool = False

    def saisir_chiffre(self, chiffre: str) -> None:
        """Ajoute un chiffre (0-9) à l'affichage courant."""
        if self._resultat_venant_d_etre_calcule:
            self.affichage = "0"
            self._resultat_venant_d_etre_calcule = False

        if self.affichage == "0":
            self.affichage = chiffre
        else:
            self.affichage += chiffre

    def saisir_virgule(self) -> None:
        """Ajoute un séparateur décimal si l'affichage n'en contient pas déjà un."""
        if self._resultat_venant_d_etre_calcule:
            self.affichage = "0"
            self._resultat_venant_d_etre_calcule = False

        if "," not in self.affichage:
            self.affichage += ","

    def choisir_operation(self, operation: Operation) -> None:
        """Mémorise l'opération choisie et l'opérande courant."""
        self._operande_en_attente = self._valeur_affichee()
        self._operation_en_attente = operation
        self._resultat_venant_d_etre_calcule = False
        self.affichage = "0"

    def calculer_resultat(self) -> None:
        """Calcule et affiche le résultat de l'opération en attente."""
        if self._operation_en_attente is None or self._operande_en_attente is None:
            return

        try:
            resultat = calculer(
                self._operande_en_attente,
                self._operation_en_attente,
                self._valeur_affichee(),
            )
        except ErreurDivisionParZero:
            self.affichage = "Erreur"
            self._operation_en_attente = None
            self._operande_en_attente = None
            self._resultat_venant_d_etre_calcule = True
            return

        self.affichage = self._formater(resultat)
        self._operation_en_attente = None
        self._operande_en_attente = None
        self._resultat_venant_d_etre_calcule = True

    def effacer(self) -> None:
        """Réinitialise complètement la machine (touche C)."""
        self._reinitialiser_etat()

    def _valeur_affichee(self) -> float:
        return float(self.affichage.replace(",", "."))

    @staticmethod
    def _formater(valeur: float) -> str:
        """Formate un résultat en évitant les décimales inutiles (ex: 4.0 -> '4')."""
        if valeur == int(valeur) and abs(valeur) < 1e15:
            texte = str(int(valeur))
        else:
            texte = f"{valeur:.10g}"
        return texte.replace(".", ",")
