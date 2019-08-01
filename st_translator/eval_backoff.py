from math import log
import re
# from tqdm import tqdm
import pickle
from functools import reduce
import mafan
from mafan import text
import itertools
import sys
import os

bos = " <bos> "
eos = " <eos> "

if len(sys.argv) < 3:
    print("Please type 2 input file name.")
    print("python eval_backoff.py [sim_file] [tra_file]")
    sys.exit()

sim_filename = sys.argv[1]
tra_filename = sys.argv[2]

sim_file = open(sim_filename, "r+", encoding="utf-8")
tra_file = open(tra_filename, "r+", encoding="utf-8")
tra_lines = tra_file.readlines()


def zng(paragraph):
    for sent in re.findall(u'[^!?。\.\!\?]+[!?。\.\!\?]?', paragraph, flags=re.U):
        yield sent


infile = open("conversions.txt", "r+", encoding="utf-8")

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

checklist = []
for key in s2t_dict:
    if len(s2t_dict[key]) > 1:
        for t in s2t_dict[key]:
            checklist.append(t)


def tokenizer(sentence, n=8):
    '''
    This function tokenizes input sentences according to the dicitionary.
    Input: a sentence or paragraph
    Output: a list of tokens from the input in order according to the original paragraph; a list of non-chinese characters from the original text.
    '''
    text, charList = prepare(sentence)
    token_list = []
    input_text = text
    for k in range(n, 0, -1):
        candidates = [input_text[i:i + k]
                      for i in range(len(input_text) - k + 1)]
        for candidate in candidates:
            if candidate in s2t_dict:
                token_list.append(candidate)
                input_text = re.sub(candidate, '', input_text)
    final = sequencer(token_list, text)
    return final, charList


def output_list(sentence_list, char_list):
    count = 0
    original = []  # sentence we want to output

    for word in sentence_list:
        if "-" in word:
            original.append(list(char_list[count]))
            count += 1
        else:
            original.append(word)
    return original


def output(sentence, char_list):
    count = 0
    original = ""  # sentence we want to output

    for char in list(sentence):
        if char == "-":
            original += char_list[count]  # append character if non-chinese
            count += 1
        else:
            original += char  # append chinese
    return original


def prepare(sentence):
    new = ""  # input to your tokenizer
    char_list = []  # punct / english to be omitted

    for char in list(sentence):
        if text.identify(char) is mafan.NEITHER:
            new += "-"  # sub - with non-chinese chars
            char_list.append(char)
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


# def add_stuff(order):
#     '''
#     This function divides the corpus into n-grams and stores them in dictionary.
#     Input: order of n-gram (like 2 for bi-gram)
#     Output: none
#     '''
#     infile = open("hk-zh.txt", "r+")  # this contains our corpus
#     start_padding = bos * order  # add padding
#     end_padding = eos * order

#     for line in tqdm(infile, total=1314726):
#         line = line.rstrip()
#         sentences = list(zng(line))  # tokenize sentence by sentence
#         for sentence in sentences:
#             candidate = start_padding + sentence + end_padding  # form sentence
#             word_list = candidate.split()
#             word_list_tokens = []
#             for word in word_list:
#                 if not(bool(re.match('^[a-zA-Z0-9]+$', word))):
#                     word_list_tokens.append(word)  # add if not chinese
#                 else:
#                     # turn non-chinese (except punc) to FW
#                     word_list_tokens.append("FW")
#             word_list = word_list_tokens
#             # extract n-grams through slicing
#             ordered = [word_list[i:i + order]
#                        for i in range(1, len(word_list) - order)]
#             # for each ngram, convert to tuple and add to dictionary
#             for ngram in ordered:
#                 ngram = tuple(ngram)
#                 if ngram not in corpus:
#                     corpus[ngram] = 1
#                 else:
#                     corpus[ngram] += 1


corpus = dict()

with open('corpus.pkl', 'rb') as fp:
    corpus = pickle.load(fp)


def convert(sentence):
    '''
    Returns list of possible mappings.
    Input: Simplified chinese sentence
    Output: List of lists. Each list has a set of possible traditional chinese tokens
    '''
    tokens, char_list = tokenizer(sentence)
    candidate_list = []
    for token in tokens:
        candidate_list.append(s2t_dict[token])
    candidate_list = output_list(candidate_list, char_list)
    return(candidate_list)


num_tokens = 4526000  # total number of tokens in corpus


def prob(word_list):
    '''
    Computes the log likelihood probability.
    Input: A sequence of words in form of list
    Output: Log probabilties
    '''
    word_list = tuple(word_list)  # change word list to tuple
    if word_list in corpus:
        # word found in dictionary
        numerator = corpus[word_list]  # get the frequency of that word list
        denominator = num_tokens  # let denominator be num tokens
        # cutoff the last word and check whether it's in corpus
        if len(word_list[:-1]) > 1 and word_list[:-1] in corpus:
            denom_list = word_list[:-1]
            denominator = corpus[denom_list]
        return log(numerator / denominator)  # log of prob
    else:
        word_list = list(word_list)  # convert it back to list
        k = len(word_list) - 1  # backoff, reduce n gram length
        if k > 0:
            # recursive function, divide the sequence into smaller n and find probs
            probs = [prob(word_list[i:i + k])
                     for i in range(len(word_list) - k + 1)]
            return sum(probs)
        else:
            # we found an unseen word
            if not(bool(re.match('^[a-zA-Z0-9]+$', word_list[0]))):
                return log(1 / num_tokens)  # return a small probability
            else:
                return prob(["FW"])  # we encountered a non-chinese word


def backoff(sentence, order):
    '''
    Calcuates log likelihood using backoff language model
    Input: Sentence and order of the n-gram
    Output: Log prob of that sentence
    '''
    score = 0
    sentences = list(zng(sentence))  # sentence tokenizer
    for sentence in sentences:
        start_padding = bos * order  # beginning padding
        end_padding = eos * order  # ending padding
        candidate = start_padding + sentence + end_padding  # add paddings
        word_list = candidate.split()
        word_list_tokens = []
        for word in word_list:
            # append only non-chinese words
            if not(bool(re.match('^[a-zA-Z0-9]+$', word))):
                word_list_tokens.append(word)
            else:
                word_list_tokens.append("FW")
        word_list = word_list_tokens
        ordered = [word_list[i:i + order]
                   for i in range(1, len(word_list) - order)]  # shingle into n-grams
        probs = [prob(x) for x in ordered]  # calculate probabilities
        score += sum(probs)  # final answer
    return score


def translate(sentence):
    '''
    Translate a given sentence to traditional
    Input: Simplified Sentence
    Output: Traditional Sentence
    '''
    candidates = convert(sentence)  # get the candidate lists
    final_sent = ""
    for words in candidates:
        if len(words) > 1:
            # many to one mappings
            score = -50000.0  # start with extreme negative value
            likely = ""
            for candidate in words:
                temp = final_sent
                temp = temp + " " + candidate  # add a candidate to temp sentence
                current_score = backoff(temp, 2)  # check perplexity
                if current_score > score:
                    # if performing good, include that
                    score = current_score
                    likely = candidate
            final_sent = final_sent + " " + likely
        else:
            final_sent = final_sent + " " + words[0]
    final_sent = final_sent.replace(" ", "")
    final_sent = add_back_spaces(sentence, final_sent)
    return final_sent


def add_back_spaces(original, current):
    current_list = list(current)
    original_list = list(original)
    # print(len(current_list))
    count = 1
    for index, char in enumerate(original_list):
        if char == " ":
            current_list[index - count] += " "
            count += 1
    current = "".join(current_list)
    return current


sentence = "早在23岁，伍兹就参与了世界上首个核反应堆Chicago Pile-1的建设，她是导师费米领导的项目团队中最年轻的一员。此外，伍兹在建立和使用实验所需的盖革计数器上起到关键作用。反应堆成功运转并达到自持状态时，她也是唯一在场的女性。曼哈顿计划中，她与费米合作；同时，她曾与第一任丈夫约翰·马歇尔（John Marshall）一同解决了汉福德区钚生产厂氙中毒的问题，并负责监督钚生产反应炉的建造和运行。"
a = translate(sentence)

total = 0
correct = 0
wrong = 0
micro_total = 0
micro_correct = 0

line_count = 0

for line in sim_file:
    line = line.rstrip()
    try:
        translated = translate(line)
    except:
        # Traceback (most recent call last):
        #     File "eval_backoff.py", line 300, in <module>
        #         translated = translate(line)
        #     File "eval_backoff.py", line 272, in translate
        #         final_sent = add_back_spaces(sentence, final_sent)
        #     File "eval_backoff.py", line 282, in add_back_spaces
        #         current_list[index - count] += " "
        #     IndexError: list index out of range
        line_count = line_count + 1
        continue
    tra_line = tra_lines[line_count].rstrip()

    line = translated.rstrip()

    if len(line) == len(tra_line):
        char_count = 0
        for c in line:
            total = total + 1
            if c == tra_line[char_count]:
                correct = correct + 1
            else:
                # print(c + tra_line[char_count])
                wrong = wrong + 1

            if tra_line[char_count] in checklist:
                micro_total += 1
                if c == tra_line[char_count]:
                    micro_correct = micro_correct + 1

            char_count = char_count + 1
    else:
        print('Error: '+str(len(line)) + ' ' + str(len(tra_line)))

    print(line_count)

    print('Correct: ' + str(correct))
    print('Wrong: ' + str(wrong))

    try:
        print('Percentage: ' + str(correct/total*100))
        print('Micro Percentage: ' + str(micro_correct/micro_total*100))
    except:
        print('No percentage.')
    line_count = line_count + 1

print('Total: ' + str(total))
print('Correct: ' + str(correct))
print('Wrong: ' + str(wrong))
print('Percentage: ' + str(correct/total*100))

print('Micro Total: ' + str(micro_total))
print('Micro Correct: ' + str(micro_correct))
print('Micro Percentage: ' + str(micro_correct/micro_total*100))

# Total: 61380785
# Correct: 61029218
# Wrong: 351567
# Percentage: 99.42723606418524
# Micro Total: 8393658
# Micro Correct: 8105369
# Micro Percentage: 96.56539496843926
