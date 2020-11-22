from state_machine import State
from util import promptForOption
from page_search import Search
from page_make_post import PostQuestion
import db_user
import db

def displayUserInfo(uid):
    # displays user information/records upon login
    questionCount, questionScoreAvg = db_user.questionsOwned(uid)
    answerCount, answerScoreAvg = db_user.answersOwned(uid)
    votesCount = db_user.votesRegistered(uid)

    print("User id: %s" % uid)
    print("User {userid} owns {qcount} question(s)"
          .format(userid = uid, qcount = questionCount))

    print("The average score for those question(s) is {avgscore}"
          .format(avgscore = questionScoreAvg))

    print("User {userid} owns {acount} answer(s)"
          .format(userid = uid, acount = answerCount))

    print("The average score for those answer(s) is {avgscore}"
          .format(avgscore = answerScoreAvg))

    print("User {userid} has {vcasts} votes registered for them"
          .format(userid = uid, vcasts = votesCount))

class Menu(State):
    def run(self):
        if (not db.guestMode):
            print("-- Your Info --")
            displayUserInfo(db.currentuid)

        print("\n-- Menu --")
        options = [
            ("Search Questions", Search),
            ("Post a Question", PostQuestion),
            ("Exit", None)
        ]

        choice = promptForOption(options)
        return options[choice][1]
