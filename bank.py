from abc import ABC, abstractmethod
from Command import DeposerCommand, RetirerCommand
import Invoker


class Observer(ABC):

    @abstractmethod
    def update(self, sujet, montant) -> None:
        """
        Receive update from subject.
        """
        pass


class HistoricObserver(Observer):
    
    def __init__(self):
        self._transaction = []
        
    def update(self, sujet, montant):
        self._transaction.append(f"{sujet}: {montant}")


class Compte:
    
    def __init__(self,nom: str,ref: str = None, _solde: int = None, utilisateur: str = None, _observer: Observer = []):
        self.nom = nom
        self.ref = ref if ref else self.nom
        self._solde = _solde if _solde else 0
        self.utilisateur = utilisateur if utilisateur else ""
        self._observer = []

    def ajouter_observer(self, observer):
        self._observer.append(observer)
        
    def _notify(self, sujet, montant):
        for observer in self._observer:
            observer.update(sujet, montant)

    
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
        self._notify("dépot",value_to_add)

    def remove_money(self, value_to_remove):
        if self._solde - value_to_remove > 0:
            self._solde -= value_to_remove
            self._notify("retrait", value_to_remove)

class CentralExchangeBank:
    def __init__(self, nom: str, _identifiant: int):
        self.nom = nom
        self._identifiant = _identifiant
        self._list_compte = []

    @property
    def list_compte(self):
        return self._list_compte

    def add_compte(self, compte: Compte):
        if compte in self._list_compte:
            raise ValueError("Le compte existe déjà dans la bank")
        else:
            self._list_compte.append(compte)

    def remove_compte(self, compte: Compte):
        self._list_compte = [c for c in self._list_compte if compte != compte]