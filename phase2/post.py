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

The post should be properly recorded in the database.

A unique id should be assigned to the post by your system,

the post type id should be set to 1 (to indicate that the post is a question),

the post creation date should be set to the current date

and the owner user id should be set to the user posting it (if a user id is provided).

The quantities Score, ViewCount, AnswerCount, CommentCount, and FavoriteCount
    are all set to zero

content license is set to "CC BY-SA 2.5".
"""

class PostQuestion(State):
    def run(self):
        print("-- Post a Question --\n")
        title = input("Title: ")
        body = input("Body: ")
        tags = inputList("Tags (space): ", " ")
        db.createPost(title, body, tags)
        return None
