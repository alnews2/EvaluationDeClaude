"""Tests unitaires du moteur de calcul (logique pure, sans IHM)."""

import pytest

from calculatrice.moteur import (
    ErreurDivisionParZero,
    MachineCalculatrice,
    Operation,
    calculer,
)


class TestCalculer:
    """Tests de la fonction pure `calculer`."""

    def test_addition(self):
        assert calculer(2, Operation.ADDITION, 3) == 5

    def test_soustraction(self):
        assert calculer(5, Operation.SOUSTRACTION, 3) == 2

    def test_multiplication(self):
        assert calculer(4, Operation.MULTIPLICATION, 3) == 12

    def test_division(self):
        assert calculer(9, Operation.DIVISION, 3) == 3

    def test_division_par_zero_leve_une_exception(self):
        with pytest.raises(ErreurDivisionParZero):
            calculer(5, Operation.DIVISION, 0)

    def test_addition_avec_flottants(self):
        assert calculer(0.1, Operation.ADDITION, 0.2) == pytest.approx(0.3)

    def test_soustraction_resultat_negatif(self):
        assert calculer(3, Operation.SOUSTRACTION, 5) == -2


class TestMachineCalculatrice:
    """Tests de la machine à états qui pilote l'affichage."""

    def test_affichage_initial_est_zero(self):
        machine = MachineCalculatrice()
        assert machine.affichage == "0"

    def test_saisie_simple_d_un_chiffre(self):
        machine = MachineCalculatrice()
        machine.saisir_chiffre("7")
        assert machine.affichage == "7"

    def test_saisie_de_plusieurs_chiffres(self):
        machine = MachineCalculatrice()
        machine.saisir_chiffre("1")
        machine.saisir_chiffre("2")
        machine.saisir_chiffre("3")
        assert machine.affichage == "123"

    def test_premier_chiffre_remplace_le_zero(self):
        machine = MachineCalculatrice()
        machine.saisir_chiffre("5")
        assert machine.affichage == "5"
        assert not machine.affichage.startswith("05")

    def test_addition_complete(self):
        machine = MachineCalculatrice()
        machine.saisir_chiffre("4")
        machine.choisir_operation(Operation.ADDITION)
        machine.saisir_chiffre("3")
        machine.calculer_resultat()
        assert machine.affichage == "7"

    def test_soustraction_complete(self):
        machine = MachineCalculatrice()
        machine.saisir_chiffre("9")
        machine.choisir_operation(Operation.SOUSTRACTION)
        machine.saisir_chiffre("4")
        machine.calculer_resultat()
        assert machine.affichage == "5"

    def test_multiplication_complete(self):
        machine = MachineCalculatrice()
        machine.saisir_chiffre("6")
        machine.choisir_operation(Operation.MULTIPLICATION)
        machine.saisir_chiffre("7")
        machine.calculer_resultat()
        assert machine.affichage == "42"

    def test_division_complete(self):
        machine = MachineCalculatrice()
        machine.saisir_chiffre("8")
        machine.choisir_operation(Operation.DIVISION)
        machine.saisir_chiffre("2")
        machine.calculer_resultat()
        assert machine.affichage == "4"

    def test_division_par_zero_affiche_erreur(self):
        machine = MachineCalculatrice()
        machine.saisir_chiffre("5")
        machine.choisir_operation(Operation.DIVISION)
        machine.saisir_chiffre("0")
        machine.calculer_resultat()
        assert machine.affichage == "Erreur"

    def test_nombre_decimal_avec_virgule(self):
        machine = MachineCalculatrice()
        machine.saisir_chiffre("3")
        machine.saisir_virgule()
        machine.saisir_chiffre("5")
        assert machine.affichage == "3,5"

    def test_double_virgule_ignoree(self):
        machine = MachineCalculatrice()
        machine.saisir_chiffre("3")
        machine.saisir_virgule()
        machine.saisir_virgule()
        machine.saisir_chiffre("5")
        assert machine.affichage == "3,5"

    def test_addition_decimale(self):
        machine = MachineCalculatrice()
        machine.saisir_chiffre("1")
        machine.saisir_virgule()
        machine.saisir_chiffre("5")
        machine.choisir_operation(Operation.ADDITION)
        machine.saisir_chiffre("2")
        machine.saisir_virgule()
        machine.saisir_chiffre("5")
        machine.calculer_resultat()
        assert machine.affichage == "4"

    def test_touche_effacer_reinitialise(self):
        machine = MachineCalculatrice()
        machine.saisir_chiffre("9")
        machine.choisir_operation(Operation.ADDITION)
        machine.saisir_chiffre("9")
        machine.effacer()
        assert machine.affichage == "0"

    def test_nouveau_calcul_apres_resultat(self):
        """Après un '=', taper un chiffre doit démarrer un nouveau nombre."""
        machine = MachineCalculatrice()
        machine.saisir_chiffre("2")
        machine.choisir_operation(Operation.ADDITION)
        machine.saisir_chiffre("2")
        machine.calculer_resultat()
        assert machine.affichage == "4"
        machine.saisir_chiffre("9")
        assert machine.affichage == "9"

    def test_chainage_d_operations(self):
        """3 + 2 = 5, puis + 4 = 9 (comportement calculatrice classique)."""
        machine = MachineCalculatrice()
        machine.saisir_chiffre("3")
        machine.choisir_operation(Operation.ADDITION)
        machine.saisir_chiffre("2")
        machine.calculer_resultat()
        assert machine.affichage == "5"
        machine.choisir_operation(Operation.ADDITION)
        machine.saisir_chiffre("4")
        machine.calculer_resultat()
        assert machine.affichage == "9"

    def test_egal_sans_operation_ne_plante_pas(self):
        machine = MachineCalculatrice()
        machine.saisir_chiffre("5")
        machine.calculer_resultat()  # aucune opération choisie : ne doit pas lever d'exception
        assert machine.affichage == "5"
