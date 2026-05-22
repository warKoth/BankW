
from Domain.Users import UserManager
from Domain.bank import *
from Domain.Command import DeposerMoneyCommand, RetirerMoneyCommand, AjouterCompteCommand
from Domain.bank import HistoricObserver
from Domain.Invoker import Invoker

class BankAPI:

    def __init__(self):
        self.UserManager = UserManager()
        self.Bank = CentralExchangeBank("MaBanque", 1)
        self.Invoker = Invoker()
        self._compte = {}

    
    def creer_user(self, nom, mdp):
        user = self.user_manager.creer_user(nom, mdp)
        return user.nom
