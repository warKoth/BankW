from abc import ABC, abstractmethod
from typing import List
from DataManager import LogManager


class Strategy(ABC):

    @abstractmethod
    def calculer_taux(self, solde: float) -> float:
        pass
    
    @abstractmethod
    def calculer_frais(self, solde: float) -> float:
        pass
    
    @abstractmethod
    def retirer_autoriser(self, solde: float, montant: float) -> bool:
        pass

class CompteInactifStrategy(Strategy):
    """Compte Inactif, en attente de typage ou de suppression"""
    def calculer_taux(self, solde: float) -> float:
        return 0
    
    def calculer_frais(self, solde: float) -> float:
        return 0
    
    def retirer_autoriser(self, solde:float, montant:float) -> bool:
        return False
    
class CompteCourantStrategy(Strategy):

    def __init__(self, decouvert_maximum: int = 500):
        self.decouvert_maximum = decouvert_maximum

    def calculer_taux(self, solde: float) -> float:
        #pas de taux
        return 0
    
    def calculer_frais(self, solde: float) -> float:
        frais_fixe = 5
        if solde < 0:
            frais_decouvert = abs(solde)*0.1/12 
            return solde - frais_decouvert - frais_fixe
        return solde - frais_fixe
    
    def retirer_autoriser(self, solde:float, montant:float) -> bool:
        return (solde - montant) >= -self.decouvert_maximum



class CompteEpargneStrategy(Strategy):

    def __init__(self, nombre_retrait_max: int = 3):
        self.nombre_retrait_max = nombre_retrait_max

    def calculer_taux(self, solde: float) -> float:
        if solde > 10000:
            return 0.03
        return 0.05
    
    def calculer_frais(self, solde: float) -> float:
        frais_fixe = 1
        if solde == 0:
            return solde
        return solde - frais_fixe
    
    def retirer_autoriser(self, solde:float, montant:float) -> bool:
        if self.nombre_retrait_max > 0 and montant < solde/3:
            self.nombre_retrait_max -= 1
            return True
        return False


class CompteInvestissementStrategy(Strategy):
    """Type de compte : investissement 
        Pour rapidement faire monter un capital mais cher à entretenir et limiter en terme de retrait """

    def __init__(self, max_retrait: float = 0.20, solde_minimum: int = 1000):
        self.max_retrait = max_retrait
        self.solde_minimum = solde_minimum

    def calculer_taux(self, solde: float) -> float:
        if solde > 20000:
            return 0.05
        return 0.07
    
    def calculer_frais(self, solde: float) -> float:
        frais_fixe = 10
        if solde == 0:
            return solde
        return solde - frais_fixe
    
    def retirer_autoriser(self, solde:float, montant:float) -> bool:
        if solde - montant < self.solde_minimum:
            return False
        if montant > solde * self.max_retrait:
            return False
        return True

class CompteJoinStrategy(Strategy):

    def __init__(self, decouvert_maximum: int = 500):
        self.decouvert_maximum = decouvert_maximum
        self.utilisateur = []

    def add_utilisateur_join(self, user: str):
        if user not in self.utilisateur:
            self.utilisateur.append(user)

    def calculer_taux(self, solde: float) -> float:
        #pas de taux
        return 0
    
    def calculer_frais(self, solde: float) -> float:
        frais_fixe = 5
        if solde < 0:
            frais_decouvert = abs(solde)*0.1/12 
            if len(self.utilisateur) > 2:
                return solde - frais_decouvert - frais_fixe*2
            return solde - frais_decouvert - frais_fixe
        
        return solde - frais_fixe
    
    def retirer_autoriser(self, solde:float, montant:float) -> bool:
        return (solde - montant) >= -self.decouvert_maximum

# Pattern Observer
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
        LogManager().log(event, f"{sujet.nom} - {montant}")

    @property
    def transactions(self):
        return self._transaction


class Compte(Subject):  

    def __init__(self, nom: str, utilisateur: str, ref: str = None, _solde: int = 0, strategy: Strategy = None):
        super().__init__()  
        self.nom = nom
        self.ref = ref if ref else self.nom
        self._solde = _solde  
        self._strategie = strategy if strategy else CompteInactifStrategy()
        self.utilisateur = [] if isinstance(self._strategie, CompteJoinStrategy) else utilisateur
        

    @property
    def strategie(self):
        return self._strategie

    @property
    def solde(self):
        return self._solde

    @solde.setter
    def solde(self, value):
        if value < 0:
            raise ValueError("Le solde ne peut pas être négatif")
        self._solde = value

    def appliquer_strategy(self, strategie):
        if isinstance(strategie, Strategy):
            self._strategie = strategie
            self.notify(f"strategie : {strategie}", 3)
    
    def appliquer_taux(self):
        taux = self._strategie.calculer_taux(self._solde)
        self.notify("Taux appliquer", 4)
        return (1+taux)*self._solde
    
    def appliquer_frais(self):
        self.notify("Frais appliquer", 5)
        self._solde = self._strategie.calculer_frais(self._solde)

    def retrait_autorise(self, montant) -> bool:
        return self._strategie.retirer_autoriser(self._solde, montant)

    def add_money(self, value_to_add):
        self._solde += value_to_add
        self.notify("dépôt", value_to_add)

    def remove_money(self, value_to_remove):
        if self.retrait_autorise(value_to_remove):  
            self._solde -= value_to_remove
            self.notify("retrait", value_to_remove)


class CentralExchangeBank(Subject):
    def __init__(self, nom: str, _identifiant: int):
        self.nom = nom
        self._identifiant = _identifiant
        self._list_compte = {}

    @property
    def list_compte(self):
        return self._list_compte

    def add_compte(self, compte: Compte, nom_user: list):
        if nom_user not in self._list_compte:
            self._list_compte[nom_user] = [compte]
        else:
            if compte in self._list_compte[nom_user]:
                raise ValueError("Le compte existe déjà dans la bank")
            self._list_compte[nom_user].append(compte)
    
        self.notify("Nouveaux compte", 00)

    def remove_compte(self, comptes: list):
        self._list_compte = {k: [c for c in v if c not in comptes] for k, v in self._list_compte.items()}
        self.notify("Suppression de compte", 1)