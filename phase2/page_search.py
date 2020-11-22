from state_machine import State
from util import inputInt, inputYesNo
import db_search

class Search(State):
    def run(self):
        print("-- Search --")
        keywords = input("Enter one or more keywords (separated by a space): ")
        keywordsList = db_search.validateKeywords(keywords, " ")
        db_search.getMatchingQuestions(keywords)
        return None

