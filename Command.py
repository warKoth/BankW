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
    def __init__(self, _bank: CentralExchangeBank, _compte):
        self._bank = _bank
        self._compte = _compte
        
    def execute(self):
        self._bank.add_compte(self._compte)
        
    def undo(self):
        self._bank.remove_compte(self._compte)
        
class RetirerCompteCommand(Command):
    def __init__(self, _bank: CentralExchangeBank, _compte):
        self._bank = _bank
        self._compte = _compte
        
    def execute(self):
        self._bank.remove_compte(self._compte)
        
    def undo(self):
        self._bank.add_compte(self._compte)
