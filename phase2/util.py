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


def inputIntRange(prompt, start:int, end:int, default = 0):
    assert(end>=start)
    num = inputInt(prompt, default)
    while(num < start or num > end):
        print("Must be in  range [{}, {}]: ".format(start, end))
        num = inputInt(prompt, default)
    return num

def promptForOption(options):
    for i, option in enumerate(options, start=1):
        print(str(i)+ ". " + option[0] )
    print("")
    return inputIntRange("Please select an option: ", 1, len(options)) - 1

