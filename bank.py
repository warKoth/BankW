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

    
