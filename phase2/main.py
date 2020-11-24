import db
from state_machine import StateMachine
from page_login import Login

from util import inputInt, inputIntRange

def main():
    port = inputIntRange("Please enter a port number (Default is 27017): ", 1, 65535, 27017)
    db.init(port)
    sm = StateMachine()
    sm.start(Login)



if __name__ == "__main__":
    main()




