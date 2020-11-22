from state_machine import State
import db
from util import inputInt, inputYesNo

def inputList(prompt, seperator):
    result = input(prompt)
    return result.split(seperator)

"""
Post a question.
The user should be able to post a question by providing:
    a title text, a body text, and zero or more tags.
"""
class PostQuestion(State):
    def run(self):
        print("-- Post a Question --\n")
        title = input("Title: ")
        body = input("Body: ")
        tags = inputList("Tags (space): ", " ") 
        db.insertPost(title, body, tags, "1")
        return None
