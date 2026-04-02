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


    


    def __init__(self,nom: str,ref: str = None, _solde: int = None, utilisateur: str = None):


class CentralExchangeBank:


    def __init__(self, nom: str, _identifiant: int):

        self.nom = nom


        self.ref = ref if ref else self.nom


        self._solde = _solde if _solde else 0


        self.utilisateur = utilisateur if utilisateur else ""


        self._observer = []


    


    def ajouter_observer(self, observer):


        self._observer.append(observer)


        self._identifiant = _identifiant


        self._list_compte = []




    def _notify(self, sujet, montant):


        for observer in self._observers:


            observer.update(sujet, montant)


            

    @property


    def solde(self):


        return self._solde


    def list_compte(self):


        return self._list_compte




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


    def add_compte(self, compte: Compte):


        if compte in self._list_compte:


            raise ValueError("Le compte existe déjà dans la bank")


        else:


            self._list_compte.append(compte)


            


    def remove_compte(self, compte: Compte):


        self._list_compte = [c for c in self._list_compte if c != compte]


        


    def exchange(self,montant: int, compte1: Compte, compte2: Compte):


        """ Echange de fond d'un compte vers un autre compte"""


        if compte1 or compte2 not in self._list_compte:


            raise ValueError("Un compte n'existe pas")


            


        if compte1._solde < montant:


            raise ValueError(f"Le solde du compte {compte1} est inférieur au montant")


            


        compte1._remove_money(montant)


        compte2.add_money(montant)


        # to add : notify

