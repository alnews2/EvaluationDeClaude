"""Tests d'intégration de l'IHM : simulent des clics réels sur les boutons Qt.

Complètent les tests unitaires du moteur en vérifiant que les clics sont
bien câblés aux bonnes actions.
"""

from PySide6.QtCore import Qt

from calculatrice.fenetre import FenetreCalculatrice


def _cliquer(qtbot, bouton_texte: str, fenetre: FenetreCalculatrice) -> None:
    """Trouve le QPushButton portant ce texte et simule un clic gauche dessus."""
    from PySide6.QtWidgets import QPushButton

    for candidat in fenetre.findChildren(QPushButton):
        if candidat.text() == bouton_texte:
            qtbot.mouseClick(candidat, Qt.MouseButton.LeftButton)
            return
    raise AssertionError(f"Bouton '{bouton_texte}' introuvable dans la fenêtre.")


def test_addition_via_clics(qtbot):
    fenetre = FenetreCalculatrice()
    qtbot.addWidget(fenetre)

    _cliquer(qtbot, "4", fenetre)
    _cliquer(qtbot, "+", fenetre)
    _cliquer(qtbot, "3", fenetre)
    _cliquer(qtbot, "=", fenetre)

    assert fenetre._label_affichage.text() == "7"


def test_division_par_zero_via_clics(qtbot):
    fenetre = FenetreCalculatrice()
    qtbot.addWidget(fenetre)

    _cliquer(qtbot, "5", fenetre)
    _cliquer(qtbot, "÷", fenetre)
    _cliquer(qtbot, "0", fenetre)
    _cliquer(qtbot, "=", fenetre)

    assert fenetre._label_affichage.text() == "Erreur"


def test_bouton_effacer_via_clics(qtbot):
    fenetre = FenetreCalculatrice()
    qtbot.addWidget(fenetre)

    _cliquer(qtbot, "9", fenetre)
    _cliquer(qtbot, "C", fenetre)

    assert fenetre._label_affichage.text() == "0"


def test_fenetre_a_le_bon_titre(qtbot):
    fenetre = FenetreCalculatrice()
    qtbot.addWidget(fenetre)
    assert fenetre.windowTitle() == "Calculatrice"
