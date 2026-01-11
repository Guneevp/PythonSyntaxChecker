import json
import random
import tokenize
from io import BytesIO
import keyword

tokens = [
    "def", "return", "if", "elif", "else", "for", "while",
    "break", "continue", "pass", "try", "except",
    "in", "is", "and", "or", "not",

    "(", ")", "[", "]", "{", "}",
    ",", ":", ".", ";",

    "+", "-", "*", "/", "//", "%", "**",

    "=", "==", "!=", "<", "<=", ">", ">=",

    "+=", "-=", "*=",

    "<NEWLINE>",
    "<INDENT>",
    "<DEDENT>",

    "<VAR>",   # identifiers
    "<NUM>",   # numbers
    "<STR>",    # strings
    "<PAD>",
    "<UNK>"
]


TOKENS_TO_ID = {v : i for i, v in enumerate(tokens)}


def tokenize_code(code: str):
    tokens = []

    try:
        for tok in tokenize.tokenize(BytesIO(code.encode()).readline):
            if tok.type in {
                tokenize.ENCODING,
                tokenize.ENDMARKER,
                tokenize.NL,
            }:
                continue

            tokens.append(normalize_token(tok.type, tok.string))

    except tokenize.TokenError:
        # still return what we got
        pass

    return tokens

def normalize_token(token_type, token_string):
    match token_type:
        case tokenize.NAME:
            if keyword.iskeyword(token_string):
                return token_string
            return "<VAR>"

        case tokenize.NUMBER:
            return "<NUM>"

        case tokenize.STRING:
            return "<STR>"
        case tokenize.NEWLINE:
            return "<NEWLINE>"
        case tokenize.INDENT:
            return "<INDENT>"
        case tokenize.DEDENT:
            return "<DEDENT>"

    return token_string

with open("C:\\Users\\gunee\\Desktop\\Projects\\Machine Learning\\data\\Python Parser\\Clean\\AllValid.json", "r") as f:
    validData = json.load(f)
with open("C:\\Users\\gunee\\Desktop\\Projects\\Machine Learning\\data\\Python Parser\\Clean\\AllInValid.json", "r") as f:
    invalidData = json.load(f)

random.seed(21)
mixedData = validData
random.shuffle(mixedData)
for unit in mixedData:
    tokenized = tokenize_code(unit["code"])
    tokenized = tokenized[:200] + ["<PAD>"] * (max(0, 200 - len(tokenized)))
    assert len(tokenized) == 200
    unit["code"] = tokenize_code(unit["code"])
with open("C:\\Users\\gunee\\Desktop\\Projects\\Machine Learning\\data\\Python Parser\\Clean\\Tokenized.json", "w") as f:
    json.dump(mixedData, f, indent=2)




print(tokenize_code("def setup(**attrs):\n    logging.configure()\n    _install_setup_requires(attrs)\n    return distutils.core.setup(**attrs)"))