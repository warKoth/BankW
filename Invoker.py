import Command

class invoker:

    def __init__(self):
        self._historique = []

    def executer(self, command):
        command.execute()
        self._historique.append(command)

    def cancel(self):
        if self._historique:
            command = self._historique.pop()
            command.undo()

        

