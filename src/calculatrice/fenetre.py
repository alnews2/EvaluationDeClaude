"""Interface graphique de la calculatrice (Qt / PySide6).

Ce module ne contient aucune logique de calcul : il délègue entièrement
à `MachineCalculatrice`. Son seul rôle est de traduire les clics en appels
au moteur, et de refléter l'état du moteur à l'écran.
"""

from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from calculatrice.moteur import MachineCalculatrice, Operation

LARGEUR_FENETRE = 320
HAUTEUR_FENETRE = 460


class FenetreCalculatrice(QWidget):
    """Fenêtre principale de la calculatrice."""

    def __init__(self) -> None:
        super().__init__()
        self._machine = MachineCalculatrice()

        self.setWindowTitle("Calculatrice")
        self.setFixedSize(LARGEUR_FENETRE, HAUTEUR_FENETRE)

        self._label_affichage = self._creer_label_affichage()

        agencement = QVBoxLayout(self)
        agencement.setContentsMargins(16, 16, 16, 16)
        agencement.setSpacing(12)
        agencement.addWidget(self._label_affichage)
        agencement.addLayout(self._creer_grille_boutons())
        agencement.addWidget(self._creer_label_mention())

        self._rafraichir_affichage()

    def _creer_label_affichage(self) -> QLabel:
        label = QLabel("0")
        label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        label.setFixedHeight(72)
        police = QFont()
        police.setPointSize(28)
        label.setFont(police)
        label.setObjectName("affichage")
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        label.setStyleSheet(
            "QLabel#affichage {"
            " border: 1px solid #a0a0a0;"
            " border-radius: 6px;"
            " background-color: #fafafa;"
            " padding-right: 12px;"
            "}"
        )
        return label

    def _creer_label_mention(self) -> QLabel:
        label = QLabel("Application générée par l'intelligence artificielle Claude de la société Anthropic.")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setWordWrap(True)
        police = QFont()
        police.setPointSize(8)
        police.setItalic(True)
        label.setFont(police)
        label.setObjectName("mentionGeneration")
        return label

    def _creer_grille_boutons(self) -> QGridLayout:
        grille = QGridLayout()
        grille.setSpacing(8)

        # Ligne 0 : C et ÷ seulement (aligné en haut à droite comme une calculatrice classique)
        grille.addWidget(self._creer_bouton("C", self._on_effacer, operateur=True), 0, 0)
        grille.addWidget(self._creer_bouton("÷", lambda: self._on_operation(Operation.DIVISION), operateur=True), 0, 3)

        grille.addWidget(self._creer_bouton("7", lambda: self._on_chiffre("7")), 1, 0)
        grille.addWidget(self._creer_bouton("8", lambda: self._on_chiffre("8")), 1, 1)
        grille.addWidget(self._creer_bouton("9", lambda: self._on_chiffre("9")), 1, 2)
        grille.addWidget(self._creer_bouton("×", lambda: self._on_operation(Operation.MULTIPLICATION), operateur=True), 1, 3)

        grille.addWidget(self._creer_bouton("4", lambda: self._on_chiffre("4")), 2, 0)
        grille.addWidget(self._creer_bouton("5", lambda: self._on_chiffre("5")), 2, 1)
        grille.addWidget(self._creer_bouton("6", lambda: self._on_chiffre("6")), 2, 2)
        grille.addWidget(self._creer_bouton("-", lambda: self._on_operation(Operation.SOUSTRACTION), operateur=True), 2, 3)

        grille.addWidget(self._creer_bouton("1", lambda: self._on_chiffre("1")), 3, 0)
        grille.addWidget(self._creer_bouton("2", lambda: self._on_chiffre("2")), 3, 1)
        grille.addWidget(self._creer_bouton("3", lambda: self._on_chiffre("3")), 3, 2)
        grille.addWidget(self._creer_bouton("+", lambda: self._on_operation(Operation.ADDITION), operateur=True), 3, 3)

        grille.addWidget(self._creer_bouton("0", lambda: self._on_chiffre("0")), 4, 0, 1, 2)
        grille.addWidget(self._creer_bouton(",", self._on_virgule), 4, 2)
        grille.addWidget(self._creer_bouton("=", self._on_egal, operateur=True), 4, 3)

        return grille

    def _creer_bouton(self, texte: str, gestionnaire, *, operateur: bool = False) -> QPushButton:
        bouton = QPushButton(texte)
        bouton.setFixedHeight(56)
        bouton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        police = QFont()
        police.setPointSize(16)
        bouton.setFont(police)
        bouton.setObjectName("boutonOperateur" if operateur else "boutonChiffre")
        bouton.clicked.connect(gestionnaire)
        return bouton

    # -- Gestionnaires d'évènements -------------------------------------

    def _on_chiffre(self, chiffre: str) -> None:
        self._machine.saisir_chiffre(chiffre)
        self._rafraichir_affichage()

    def _on_virgule(self) -> None:
        self._machine.saisir_virgule()
        self._rafraichir_affichage()

    def _on_operation(self, operation: Operation) -> None:
        self._machine.choisir_operation(operation)
        self._rafraichir_affichage()

    def _on_egal(self) -> None:
        self._machine.calculer_resultat()
        self._rafraichir_affichage()

    def _on_effacer(self) -> None:
        self._machine.effacer()
        self._rafraichir_affichage()

    def _rafraichir_affichage(self) -> None:
        self._label_affichage.setText(self._machine.affichage)


def lancer_application() -> None:
    """Point d'entrée : lance l'application Qt."""
    app = QApplication(sys.argv)
    fenetre = FenetreCalculatrice()
    fenetre.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    lancer_application()
