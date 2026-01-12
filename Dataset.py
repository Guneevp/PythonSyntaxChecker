import json
import math
import random
import tokenize
from io import BytesIO
import keyword

import torch
from torch.utils.data import DataLoader

import invalidData

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

random.seed(21)

good_tokens = []
good_tokens_attention_mask = []

bad_tokens = []
bad_tokens_attention_mask = []

mixedData = validData
random.shuffle(mixedData)
for unit in validData:
    tokenized = tokenize_code(unit["code"])
    tokenized = tokenized[:200]
    to_pad_length = (max(0, 200 - len(tokenized)))
    tokenized += ["<PAD>"] * to_pad_length
    assert len(tokenized) == 200
    attention_mask = [1] * (200 - to_pad_length) + [0] * to_pad_length

    good_tokens.append(tokenized)
    good_tokens_attention_mask.append(attention_mask)


    tokenized_errorized = invalidData.create_random_error(tokenized)[:200]
    if tokenized_errorized is not None:
        to_pad_length = (max(0, 200 - len(tokenized_errorized)))
        tokenized_errorized += ["<PAD>"] * to_pad_length
        assert len(tokenized_errorized) == 200
        bad_tokens.append(tokenized_errorized)
        attention_mask = [1] * (200 - to_pad_length) + [0] * to_pad_length
        bad_tokens_attention_mask.append(attention_mask)

assert abs((len(good_tokens) - len(bad_tokens)) / len(good_tokens)) < 0.1 # if the size is not similar the model will just learn to always guess valid


tokens = [[TOKENS_TO_ID.get(j, TOKENS_TO_ID["<UNK>"]) for j in i] for i in good_tokens] + [[TOKENS_TO_ID.get(j, TOKENS_TO_ID["<UNK>"]) for j in i] for i in bad_tokens]
attention_mask = good_tokens_attention_mask + bad_tokens_attention_mask
labels = len(good_tokens_attention_mask) * [1] + len(bad_tokens_attention_mask) * [0]
random.seed(21)
random.shuffle(tokens)
random.seed(21)
random.shuffle(attention_mask)
random.seed(21)
random.shuffle(labels)



class SyntaxCodeDataSet(torch.utils.data.Dataset):

    def __init__(self, data_tensor, attention_mask, labels):
        self.data_tensor = data_tensor
        self.attention_mask = attention_mask
        self.labels = labels

    def __getitem__(self, item):
        return {
            "input_ids" : self.data_tensor[item],
            "attention_mask" : self.attention_mask[item],
            "label" : self.labels[item]

        }

    def __len__(self):
        return len(self.labels)

dataset = SyntaxCodeDataSet(torch.tensor(tokens), torch.tensor(attention_mask), torch.tensor(labels))

loader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,
    drop_last=False
)


