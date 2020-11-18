from state_machine import State
from menu import Menu
import db

def inputYesNo(prompt):
    answer = ""
    prompt += " [y/yes/n/no]: "
    while (answer not in ["yes", "y", "no", "n"]):
        answer = input(prompt)
    return (answer in ["yes", "y"])

class Login(State):
    def run(self):
        print("-- Login --")
        guest = inputYesNo("Login as a guest? ")
        if (guest):
            db.guestLogin()
            return Menu

        register = inputYesNo("Would you like to register?")
        if (register):
            return Login

        loginSuccess = False
        while not loginSuccess:
            uid = input("Username: ")
            password = input("Password: ")
            loginSuccess = db.login(uid, password)
        return Menu
