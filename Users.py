from abc import ABC, abstractmethod

class User:
    """ Class User permettant de créer des utilisateurs avec des accès dédié"""

    def __init__(self, id:int, nom:str, _mdp:str=None):
        self.id = id
        self.nom = nom
        self._mdp = _mdp if _mdp else self.nom
        self.list_compte = {}

    @property
    def mdp(self):
        return self._mdp
    
    def change_mdp(self, new_value_mdp):
        actual_mdp_true = input("Mot de passe actuel (Identitifiant si première connexion) ? \n")
        if actual_mdp_true == self._mdp:
            self._mdp = new_value_mdp
            return ("Mot de passe changé !")
    
    def new_compte(self, nom: str, solde: int = 0):
        if nom in self.list_compte:
            raise ValueError("Un compte de ce nom existe déjà !")
        
        self.list_compte[nom] = solde

    def delete_compte(self, nom:str):
        actual_mdp_true = input("Mot de passe actuel (Identitifiant si première connexion) ? \n")
        if actual_mdp_true == self._mdp:
            self.list_compte = {k:v for k,v in self.list_compte.items() if k != nom}