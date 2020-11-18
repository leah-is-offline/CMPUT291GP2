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


