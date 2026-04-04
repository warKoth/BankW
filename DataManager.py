import sqlite3
import datetime


class DataBaseManager:
    _instance = None

    def __new__(cls, db_name: str = "BankWPersitance.db"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialiser(db_name)
        return cls._instance
    
    def _initialiser(self, db_name:str):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")
        self.create_tables()


    def create_tables(self):

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                mdphash TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS compte (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                ref INTEGER NOT NULL,
                solde INTEGER,
                strategie TEXT NOT NULL             
            )                   
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_compte (
                user_id INTEGER NOT NULL,
                compte_id INTEGER NOT NULL,
                PRIMARY KEY (user_id, compte_id),
                FOREIGN KEY (user_id) REFERENCES user(id),
                FOREIGN KEY (compte_id) REFERENCES compte(id)
            )
        ''')

        self.conn.commit()


    def creer_user(self, nom: str, mdphash: str):
        self.cursor.execute(
            "INSERT INTO user (nom, mdphash) VALUES (?, ?)",
            (nom, mdphash)
                         
        )
        self.conn.commit()

    def get_user(self, nom: str):
        self.cursor.execute(
            "SELECT * FROM user WHERE nom = ?",
            (nom,)

        )
        return self.cursor.fetchone()
    
    def supprime_user(self, user_id: int):
        self.cursor.execute("DELETE FROM user_compte WHERE user_id = ?", (user_id,))
        self.cursor.execute(
            "DELETE FROM user WHERE id = ?",
            (user_id, )
        )
        self.conn.commit()

    def creer_compte(self, nom: str, ref: int, solde: int, strategie: str):
        self.cursor.execute(
            "INSERT INTO compte (nom, ref, solde, strategie) VALUES (?, ?, ?, ?)",
            (nom, ref, solde, strategie)
        )
        self.conn.commit()

    def get_compte(self, nom: str, ref: int):
        self.cursor.execute(
            "SELECT * FROM compte WHERE nom = ? AND ref = ?",
            (nom, ref)
        )
        return self.cursor.fetchone()
    
    def supprime_compte(self, compte_id: int):
        self.cursor.execute(
            "DELETE FROM user_compte WHERE compte_id = ?", 
            (compte_id,)
        )
        self.cursor.execute(
            "DELETE FROM compte WHERE compte_id",
            (compte_id,)
        )
        self.conn.commit()

    
    def lier_compte_user(self, compte_id: int, user_id: int):
        self.cursor.execute(
            "INSERT INTO user_compte (user_id, compte_id) VALUES (?, ?)",
            (user_id, compte_id)
        )
        self.conn.commit()

    def get_compte_user(self, compte_id: int):
        self.cursor.execute(
            "SELECT * FROM user_compte WHERE compte_id = ?",
            (compte_id, )
        )
        self.cursor.fetchall()

    def close(self):
        self.conn.close() 


# log manager pour l'historique
class LogManager: 
    _instance = None

    def __new__(cls, log_file: str = "bank.log"):# pattern singletton
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialiser(log_file)
        return cls._instance

    def _initialiser(self, log_file: str): 
        self._log_file = log_file

    def log(self, event: str, details: str): #écrit les logs
        with open(self._log_file, "a") as f:
            f.write(f"{datetime.datetime.now()} - {event} : {details}\n")