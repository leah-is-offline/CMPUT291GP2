from state_machine import State
from util import inputInt

class Menu(State):
    def run(self):
        print("--Menu--")
        print("1. Search Questions"
            + "\n2. Post Questions"
            + "\n3. Exit"
        )

        option = inputInt("Option: ")
        switch = {
            3: None
        }
        return switch.get(option, Menu)
