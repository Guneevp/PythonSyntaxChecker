import ast
import json
import random
from typing import Optional


def create_random_error(code: list[str]) -> Optional[list[str]]:
    code = code.copy()
    choice = random.randint(0, 1)
    match choice:
        case 0:
            # Removing a character
            choice2 = random.randint(0, 1)
            match choice2:
                case 0:
                    # Remove random paranthesis
                    matching = random.choice("()")

                case 1:
                    # Random colon
                    matching = ":"
                case 2:
                    matching = "\n" # breaks python tokenizer
            index = [i for i, v in enumerate(code) if v == matching]
            index = random.choice(index)
            code.pop(index)
        case 1:
            # Adding random character
            match = ":()"
            match = random.choice(match)
            index = random.randint(0, len(code) - 1)
            code.insert(index, match)
    try:
        ast.parse("".join(code))
    except SyntaxError:
        return code




if __name__ == "__main__":
    with open("C:\\Users\\gunee\\Desktop\\Projects\\Machine Learning\\data\\Python Parser\\Clean\\AllValid.json", "r") as f:
        data = json.load(f)
        random.seed(21)
        modified_data = []
        for i in data:
            error = create_random_error(i)
            if error is not None:
                modified_data.append((error))
        with open("C:\\Users\\gunee\\Desktop\\Projects\\Machine Learning\\data\\Python Parser\\Clean\\AllInValid.json", "w") as r:
            json.dump(modified_data, r, indent=2)