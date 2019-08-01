import re
import pickle
from functools import reduce
import mafan
from mafan import text
import itertools
from tqdm import tqdm

infile = open("conversions.txt", "r+")

from opencc import OpenCC

s2t_dict = dict()

for line in infile:
    line = line.rstrip()
    arr = line.split()
    trad = arr[0]
    sim = arr[1]
    if sim not in s2t_dict:
        s2t_dict[sim] = [trad]
    else:
        s2t_dict[sim].append(trad)
s2t_dict['-'] = ['-']

def sequencer(tokens, example):

    flags = [1] * len(example)
    sequence = []
    for token in tokens:
        for match in re.finditer(token, example):
            location = (token, match.span()[0], match.span()[1])
            valid = reduce(lambda x,y:x*y, flags[location[1]:location[2]])
            if valid:
                sequence.append(location)
                for i in range(location[1], location[2]):
                    flags[i] = 0
            else:
                continue
    sequence.sort(key=lambda x: x[1])
    result = [x[0] for x in sequence]
    return result

def prepare(sentence):
    new = "" # input to your tokenizer
    char_list = [] # punct / english to be omitted

    for char in list(sentence):
        if text.identify(char) is mafan.NEITHER:
            new += "-" # sub - with non-chinese chars
            char_list.append(char)
        else:
            new += char

    return new, char_list

def output(sentence, char_list):
    count = 0
    original = "" # sentence we want to output

    for char in list(sentence):
        if char == "-":
            original += char_list[count] # append character if non-chinese
            count += 1
        else:
            original += char # append chinese
    return original

def tokenized(sentence, n = 8):
    text, charList = prepare(sentence)
    token_list = []
    input_text = text
    for k in range(n, 0, -1):
        candidates = [input_text[i:i + k] for i in range(len(input_text) - k + 1)]
        for candidate in candidates:
            if candidate in s2t_dict:
                token_list.append(candidate)
                input_text = re.sub(candidate, '', input_text)
    final = sequencer(token_list, text)
    return final, charList

def convert_sim(sentence):
    '''
    Translate and tokenize
    '''
    cc = OpenCC('t2s')
    converted = cc.convert(sentence)
    tokens, char_list = tokenized(converted)
    string_spaced = " ".join(x for x in tokens)
    answer = output(string_spaced, char_list)
    return answer
