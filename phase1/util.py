def inputPort(prompt, default = 0):
    num = default
    while True:
        try:
            inStr = input(prompt)
            if (inStr == ""):
                break
            num = int(inStr)
            
            if num in range(1,65536):
                break
            else:
                print("Port must be an integer between 0 and 65535")
                continue
            
        except ValueError:
            print("Invalid, expected an integer. Try again")
            continue
        else:
            break
    return num

def inputIntRange(prompt, start:int, end:int, default = 0):
    assert(end>=start)
    num = inputInt(prompt, default)
    while(num < start or num > end):
        print("Must be in  range [{}, {}]: ".format(start, end))
        num = inputInt(prompt, default)
    return num

def inputInt(prompt, default = 0):
    num = default
    while True:
        try:
            inStr = input(prompt)
            if (inStr == ""):
                break
            num = int(inStr)
        except ValueError:
            print("Invalid, expected an integer. Try again")
            continue
        else:
            break
    return num

