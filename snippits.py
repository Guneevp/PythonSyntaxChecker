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
                    with open(os.path.join(rootDir, fileName), "r") as f:
                        syntax_tree = ast.parse(f.read())
                        for node in syntax_tree.body:
                            if isinstance(node, ast.FunctionDef):
                                function_defs.append(ast.unparse(node))
                except SyntaxError:
                    continue
    return function_defs


get_all_functions("C:\\Users\\gunee\\Desktop\\University\\Winter 2024-2025 Term\\CSC148\\assignments\\a1\\starter_code")


def filter_to_short_functions(function_defs: list[str], maxLines: int) -> list[str]:
    return [f for f in function_defs if len(f.splitlines()) <= maxLines]

def save_functions_to_disk(function_defs: list[str]) -> None:


filter_to_short_functions()


print(function_defs)