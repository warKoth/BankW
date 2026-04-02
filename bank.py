from abc import ABC, abstractmethod
from typing import List
import Command
import Invoker

class Observer(ABC):

    @abstractmethod
    def update(self, sujet, event: str, montant: int) -> None:
        pass


class Subject(ABC):
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, event: str, value: int):
        for observer in self._observers:
            observer.update(self, event, value)  

class HistoricObserver(Observer):

    def __init__(self):
        self._transaction = []

    def update(self, sujet, event: str, montant: int):  
        self._transaction.append(f"{sujet.nom} - {event}: {montant}")

    @property
    def transactions(self):
        return self._transaction


class Compte(Subject):  

    def __init__(self, nom: str, ref: str = None, _solde: int = 0, utilisateur: str = ""):
        super().__init__()  
        self.nom = nom
        self.ref = ref if ref else self.nom
        self._solde = _solde  
        self.utilisateur = utilisateur

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
        self.notify("dépôt", value_to_add)

    def remove_money(self, value_to_remove):
        if self._solde - value_to_remove >= 0:  
            self._solde -= value_to_remove
            self.notify("retrait", value_to_remove)


class CentralExchangeBank(Subject):
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
            self.notify("Nouveaux compte", 00)

    def remove_compte(self, compte: Compte):
        self._list_compte = [c for c in self._list_compte if c != compte]  
        self.notify("Suppréssion de compte")