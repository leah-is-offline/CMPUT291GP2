from state_machine import State
import db
from util import inputInt, inputYesNo, promptForOption
from page_view_post import ViewPost

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
        # import here
        # because python cant handle circluar dependencies
        from page_menu import Menu

        print("-- Post a Question --\n")
        title = input("Title: ")
        body = input("Body: ")
        tags = inputList("Tags (space seperated): ", " ")
        resultPost = db.insertPost(title, body, tags, "1")

        print("\nNice! Your question has been posted.")
        print("What would you like to do now?\n")

        options = [
            ("View the post", ViewPost),
            ("Post another Question", PostQuestion),
            ("Back to menu", Menu)
        ]

        choice = promptForOption(options)
        ViewPost.postId = resultPost["Id"]

        return options[choice][1]



class PostAnswer(State):
    questionId = None
    def run(self):
        from page_menu import Menu

        if (PostAnswer.questionId == None):
            print('questionId must be staticly defined to use this class!')
            return None

        post = db.getPost(PostAnswer.questionId)

        print("-- Post an Answer --\n")
        print("-- Question --\n")

        if (post == None):
            print("No such post in databse")
        else:
            for key, value in post.items():
                print('{:15} {}'.format(key+':', value))

        print("\n -- Answer --\n")

        title = input("Title: ")
        body = input("Body: ")
        tags = inputList("Tags (space seperated): ", " ")
        resultPost = db.insertPost(title, body, tags, "2")

        print("\nNice! Your Answer has been posted.")
        print("What would you like to do now?\n")


