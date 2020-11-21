from state_machine import State
from menu import Menu
import db
from util import inputInt, inputYesNo

class Login(State):
    def run(self):
        print("-- Login --")

        guest = inputYesNo("\nLogin as a guest? ")
        #if user entered : yes or y, true. Else, false
        if (guest):
            db.guestLogin()
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

        return Menu
