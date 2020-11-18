from state_machine import State, StateMachine
from login import Login

def main():
    sm = StateMachine()
    sm.start(Login)

if __name__ == "__main__":
    main()
