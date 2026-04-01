from abc import ABC, abstractmethod
from bank import Compte

class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

class DeposerCommand(Command):
    def __init__(self, compte, value: float):
        self._compte = compte
        self._value = value

    def execute(self):
        self._compte.add_money(self._value)

    def undo(self):
        self._compte.remove_money(self._value)

class RetirerCommand(Command):
    def __init__(self, compte, value: float):
        self._compte = compte
        self._value = value

    def execute(self):
        self._compte.remove_money(self._value)

    def undo(self):
        self._compte.add_money(self._value)