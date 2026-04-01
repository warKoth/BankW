from abc import ABC, abstractmethod
from Command import DeposerCommand, RetirerCommand
import Invoker

class Compte:
    
    def __init__(self,nom: str,ref: str = None, _solde: int = None, utilisateur: str = None):
        self.nom = nom
        self.ref = ref if ref else ref = self.nom
        self._solde = _solde if _solde else _solde = 0
        self.utilisateur = utilisateur if utilisateur else utilisateur = ""

    @property
    def solde(self):
        return self._solde
    
    @solde.setter
    def solde(self, value):
        if value < 0:
            raise ValueError("Le solde ne peut pas être négatif")
        self._solde = value

    def add_money(self, value_to_add):
        self._solde += value_to_add
        # to add : notify

    def remove_money(self, value_to_remove):
        if self._solde - value_to_remove > 0:
            self._solde -= value_to_remove
            # to add : notify

    