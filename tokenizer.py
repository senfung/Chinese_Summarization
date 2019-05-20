import re
import mafan
from mafan import text
from functools import reduce

input_filename = "./datasets/LCSTS/summaries.txt"
output_filename = "./datasets/LCSTS/summaries_tok.txt"

input_file = open(input_filename, "r+")
output_file = open(output_filename, "a+")

infile = open("./st_translator/conversions.txt", "r+")

s2t_dict = dict()

for line in infile:
    line = line.rstrip()
    arr = line.split()
    trad = arr[1]
    sim = arr[0]
    if sim not in s2t_dict:
        s2t_dict[sim] = [trad]
    else:
        s2t_dict[sim].append(trad)
s2t_dict['-'] = ['-']


def prepare(sentence):
    new = ""  # input to your tokenizer
    char_list = []  # punct / english to be omitted

    for char in list(sentence):
        if text.identify(char) is mafan.NEITHER:
            new += "-"  # sub - with non-chinese chars
            char_list.append(char)
            continue
        else:
            new += char

    return new, char_list


def sequencer(tokens, example):

    flags = [1] * len(example)
    sequence = []
    for token in tokens:
        for match in re.finditer(token, example):
            location = (token, match.span()[0], match.span()[1])
            valid = reduce(lambda x, y: x*y, flags[location[1]:location[2]])
            if valid:
                sequence.append(location)
                for i in range(location[1], location[2]):
                    flags[i] = 0
            else:
                continue
    sequence.sort(key=lambda x: x[1])
    result = [x[0] for x in sequence]
    return result


def tokenizer(sentence, original, n=8):
    text, charList = prepare(sentence)
    token_list = []
    input_text = text
    for k in range(n, 0, -1):
        candidates = [input_text[i:i + k]
                      for i in range(len(input_text) - k + 1)]

        for candidate in candidates:
            if '-' in candidate:
                continue
            elif candidate in s2t_dict:
                token_list.append(candidate)
                input_text = re.sub(candidate, '', input_text)
    token_set = list(set(token_list))

    sentence_parts = sentence.split()
    ordered_parts = sequencer(sentence_parts, original)

    string = " ".join(x for x in ordered_parts)

    final = sequencer(token_set, string)
    return final, charList


token_line = False
original = ""
count = 0
for line in input_file:
    print(count)
    line = line.rstrip()

    if token_line:
        try:
            tokens, char_list = tokenizer(line, original)
            string = " ".join(x for x in tokens)

            output_file.write(original)
            output_file.write("\n")
            output_file.write(string)
            output_file.write("\n")
        except:
            print('Error. Skip.')

    else:
        original = line

    token_line = not token_line

    count = count + 1
