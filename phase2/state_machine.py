import os

class State:
    def cls(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def _run(self):
        self.cls()
        return self.run()

    def run(self):
        pass

class StateMachine:
    def start(self, stateClass):
        while stateClass != None:
            stateClass = stateClass()._run()
