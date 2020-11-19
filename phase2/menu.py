from state_machine import State
from util import inputInt
from search import Search
from post import PostQuestion

class Menu(State):
    def run(self):
        print("--Menu--")
        options = [
            ("Search Questions", Search),
            ("Post a Question", PostQuestion),
            ("Exit", None)
        ]

        for i, option in enumerate(options, start=1):
            print(str(i)+ ". " + option[0] )
        print()

        choice = inputInt("Please select an option: ")
        while(choice < 1 or choice >= len(options)):
            choice = inputInt("Not in range: ")

