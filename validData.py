import json
import os
import ast
import random

VALID_SNIPPETS = [
    "def add(a, b):\n    return a + b",
    "for i in range(5):\n    print(i)",
    "if x > 0:\n    print('positive')",
    "def square(x):\n    return x * x",
    "while n > 0:\n    n -= 1",
]


def get_all_functions(path_to_root : str) -> list[str]:
    function_defs = []
    for rootDir, subDirs, fileNames in os.walk(path_to_root):
        for fileName in fileNames:
            print(fileName)
            if fileName.endswith(".py"):
                try:
                    with open(os.path.join(rootDir, fileName), "r", encoding="utf-8") as f:
                        syntax_tree = ast.parse(f.read())
                        for node in syntax_tree.body:
                            if isinstance(node, ast.FunctionDef):
                                if node.decorator_list: continue
                                remove_docstring(node)
                                function_defs.append(ast.unparse(node))
                except (SyntaxError, UnicodeDecodeError):
                    continue
    return function_defs



def remove_docstring(node):
    if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
    ):
        node.body.pop(0)


def filter_to_short_functions(function_defs: list[str], maxLines: int) -> list[str]:
    return [f for f in function_defs if 3 <= len(f.splitlines()) <= maxLines]

def save_functions_to_disk(function_defs: list[str]) -> None:
    to_disk = [{"code": code, "label": True} for code in function_defs]
    random.seed(21)
    random.shuffle(to_disk)
    to_disk = to_disk[:3000]
    with open("C:\\Users\\gunee\\Desktop\\Projects\\Machine Learning\\data\\Python Parser\\Clean\\AllValid.json", "w") as f:
        json.dump(to_disk, f, indent=2)


save_functions_to_disk(filter_to_short_functions(get_all_functions("C:\\Users\\gunee\\Desktop\\Projects\\Machine Learning\\data\\Python Parser\\Raw"), 30))

