from state_machine import State, StateMachine
from login import Login
import db
from util import inputInt

def main():
    port = inputInt("Please enter a port number (Default is 27012): ", 27017)
    db.init(port)
    sm = StateMachine()
    sm.start(Login)

if __name__ == "__main__":
    main()
