from abc import ABC, abstractmethod
from bank import Compte, CentralExchangeBank

class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

class DeposerMoneyCommand(Command):
    def __init__(self, compte, value: float):
        self._compte = compte
        self._value = value

    def execute(self):
        self._compte.add_money(self._value)

    def undo(self):
        self._compte.remove_money(self._value)

class RetirerMoneyCommand(Command):
    def __init__(self, compte, value: float):
        self._compte = compte
        self._value = value

    def execute(self):
        self._compte.remove_money(self._value)

    def undo(self):
        self._compte.add_money(self._value)
        
class AjouterCompteCommand(Command):
    def __init__(self, _bank: CentralExchangeBank, _nom_user: str, _compte: Compte):
        self._bank = _bank
        self._nom_user = _nom_user
        self._compte = _compte
        
    def execute(self):
        self._bank.add_compte(self._compte, self._nom_user)
        
    def undo(self):
        self._bank.remove_compte(self._compte)
        
class RetirerCompteCommand(Command):
    def __init__(self, _bank: CentralExchangeBank, _nom_user: str, _compte: Compte):
        self._bank = _bank
        self._nom_user = _nom_user
        self._compte = _compte
        
    def execute(self):
        self._bank.remove_compte(self._compte, self._nom_user)
        
    def undo(self):
        self._bank.add_compte(self._compte, self._nom_user)
        
class ExchangeMoneyCommand(Command):
    def __init__(self, _value: int, _compte1: Compte, _compte2: Compte):
        self._value = _value
        self._compte1 = _compte1
        self._compte2 = _compte2

    def execute(self):
        self._compte1.remove_money(self._value)
        self._compte2.add_money(self._value)

    def undo(self):
        self._compte2.remove_money(self._value)
        self._compte1.add_money(self._value)
