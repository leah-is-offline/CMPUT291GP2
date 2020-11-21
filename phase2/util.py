def inputYesNo(prompt):
    answer = ""
    prompt += " [y/yes/n/no]: "
    while (answer not in ["yes", "y", "no", "n"]):
        answer = input(prompt)
    return (answer in ["yes", "y"])

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

    

