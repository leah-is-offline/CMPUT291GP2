from state_machine import State
import db
from util import inputInt, inputYesNo
import searchUtils 


class Search(State):
    def run(self):
        print("-- Search --")
        keywords = input("Enter one or more keywords (separated by a space): ")
        keywordsList = searchUtils.validateKeywords(keywords, " ")
        db.search(keywordsList)
        return None

