from state_machine import State
from util import promptForOption
from page_search import Search
from page_make_post import PostQuestion
import db


class Menu(State):
    def run(self):
        #if (not db.guestMode):
            #print("-- Your Info --")
            #displayUserInfo(db.currentuid)

        print("\n-- Menu --")
        options = [
            ("Search Questions", Search),
            ("Post a Question", PostQuestion),
            ("Exit", None)
        ]

        choice = promptForOption(options)
        return options[choice][1]
