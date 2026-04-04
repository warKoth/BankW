from DataManager import DataBaseManager, LogManager
import bcrypt
from typing import Union

class User:
    def __init__(self, id: int, nom: str, mdp_hash: Union[str, bytes]):
        self.id = id
        self.nom = nom
        self._mdp_hash = mdp_hash if isinstance(mdp_hash, bytes) else mdp_hash.encode('utf-8')

    def verifier_mdp(self, mdp: str) -> bool:
        import bcrypt
        return bcrypt.checkpw(mdp.encode(), self._mdp_hash)

    def changer_mdp(self, ancien_mdp: str, nouveau_mdp: str) -> bool:
        import bcrypt
        if self.verifier_mdp(ancien_mdp):
            self._mdp_hash = bcrypt.hashpw(nouveau_mdp.encode(), bcrypt.gensalt())
            return True
        return False
    


class UserManager:
    _instance = None

    def __new__(cls):
        if cls._instance == None:
            cls._instance = super().__new__(cls)
            cls._instance._initialiser()
        return cls._instance

    def _initialiser(self):
        self._db = DataBaseManager()
        self._log = LogManager()
        self._users: dict = {}

    def creer_user(self, nom: str, mdp: str):
        mdphash = bcrypt.hashpw(mdp.encode(), bcrypt.gensalt())
        self._db.creer_user(nom, mdphash)
        self._log.log("User créé", f"Ajout de {nom}")
        user = User(self._db.get_user(nom)[0], nom, mdphash)
        self._users[nom] = user
        return user
    
    def connexion(self, nom: str, mdphash: str) -> User:
        if nom in self._users: #si le user est en cache 
            user = self._users[nom]
        else: #verification server
            data = self._db.get_user(nom)
            if data is None:
                raise ValueError(f"Utilisateur {nom} introuvable")
            user = User(data[0], data[1], data[2])
            self._users[nom] = user 

        if not bcrypt.checkpw(mdphash.encode(), user._mdp_hash):# check mot de passe
            raise ValueError("Mot de passe incorrect")

        self._log.log("Connexion", f"{nom} connecté")
        return user
    
    def supprimer_user(self, nom: str, mdp: str):
        data = self._db.get_user(nom)
        if data is None:
            raise ValueError("Utilisateur introuvable !")
        
        mdphash_bytes = str(data[2]).encode('utf-8')
        if not bcrypt.checkpw(mdp.encode(), mdphash_bytes):
            raise ValueError("Mot de passe incorrect !")
    
        user_id = data[0]
        self._db.supprime_user(user_id)
    
        # 4. supprimer du cache
        if nom in self._users:
            self._users = {k: v for k, v in self._users.items() if k != nom}
    
        self._log.log("Suppression", f"Utilisateur {nom} supprimé")