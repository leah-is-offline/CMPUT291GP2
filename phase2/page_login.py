from state_machine import State
from page_menu import Menu
from util import inputInt, inputYesNo
import db
import db_user

class Login(State):
    def run(self):
        print("-- Login --")
        guest = inputYesNo("\nLogin as a guest? ")
        #if user entered : yes or y, true. Else, false
        if (guest):
            db.guestLogin()
            # got to the menu
            return Menu

        register = inputYesNo("\nWould you like to register?")
        #if user entered : yes or y, true. Else, false
        if (register):
            uid = inputInt("New uid: ")
            while not db.register(uid):
                uid = inputInt("Unable to Register uid. Try another: ")
            return Menu

        uid = inputInt("\nLogin uid: ")
        while not db.login(uid):
            uid = inputInt("Login failed. Try again. uid: ")
        displayUserInfo(db.currentuid)

        return Menu


def displayUserInfo(uid):
    # displays user information/records upon login
    questionCount, questionScoreAvg ,answerCount, answerScoreAvg = db_user.questionsAnswersOwned(uid)
    votesCount = db_user.votesRegistered(uid)

    print("User id: %s" % uid)
    print("User {userid} owns {qcount} question(s)"
          .format(userid = uid, qcount = questionCount))

    print("The average score for those question(s) is {avgscore:.2f}"
          .format(avgscore = questionScoreAvg))

    print("User {userid} owns {acount} answer(s)"
          .format(userid = uid, acount = answerCount))

    print("The average score for those answer(s) is {avgscore:.2f}"
          .format(avgscore = answerScoreAvg))

    print("User {userid} has {vcasts} votes registered for them"
          .format(userid = uid, vcasts = votesCount))

    print("-- Your Info --")
    
