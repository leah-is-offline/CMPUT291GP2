from state_machine import State
import db
from util import inputInt, inputYesNo

class PostQuestion(State):
    def run(self):
        print("-- Post a question --")

