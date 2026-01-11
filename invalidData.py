import ast
import json
import random


def create_random_error(function: dict):
    code = function["code"]
    choice = random.randint(0, 1)
    match choice:
        case 0:
            # Removing a character
            choice2 = random.randint(0, 2)
            match choice2:
                case 0:
                    # Remove random paranthesis
                    matching = "()"
                case 1:
                    # Random colon
                    matching = ":"
                case 2:
                    matching = "\n"
            index = [i for i, v in enumerate(code) if v in matching]
            index = random.choice(index)
            function["code"] = code[:index] + code[index + 1:]
        case 1:
            # Adding random character
            match = ":()\n"
            match = random.choice(match)
            index = random.randint(0, len(code) - 1)
            function["code"] = code[:index] + match + code[index + 1:]
    try:
        ast.parse(function["code"])
    except SyntaxError:
        function["label"] = False
        return function





with open("C:\\Users\\gunee\\Desktop\\Projects\\Machine Learning\\data\\Python Parser\\Clean\\AllValid.json", "r") as f:
    data = json.load(f)
    random.seed(21)
    modified_data = [create_random_error(i) for i in data]
    with open("C:\\Users\\gunee\\Desktop\\Projects\\Machine Learning\\data\\Python Parser\\Clean\\AllInValid.json", "w") as r:
        json.dump(modified_data, r, indent=2)