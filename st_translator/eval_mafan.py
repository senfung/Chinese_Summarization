import sys
import os
from mafan import tradify

if len(sys.argv) < 3:
    print("Please type 2 input file name.")
    print("python eval_mafan.py [sim_file] [tra_file]")
    sys.exit()

sim_filename = sys.argv[1]
tra_filename = sys.argv[2]

sim_file = open(sim_filename, "r+", encoding="utf-8")
tra_file = open(tra_filename, "r+", encoding="utf-8")
tra_lines = tra_file.readlines()

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

total = 0
correct = 0
wrong = 0
micro_total = 0
micro_correct = 0

line_count = 0

for line in sim_file:

    line = line.rstrip()
    line = tradify(line)
    tra_line = tra_lines[line_count].rstrip()

    if len(line) == len(tra_line):
        char_count = 0
        for c in line:
            total = total + 1
            if c == tra_line[char_count]:
                correct = correct + 1
            else:
                wrong = wrong + 1

            if tra_line[char_count] in checklist:
                micro_total += 1
                if c == tra_line[char_count]:
                    micro_correct = micro_correct + 1

            char_count = char_count + 1

    print(line_count)

    line_count = line_count + 1

print('Total: ' + str(total))
print('Correct: ' + str(correct))
print('Wrong: ' + str(wrong))

print('Percentage: ' + str(correct/total*100))
print('Micro Total: ' + str(micro_total))
print('Micro Correct: ' + str(micro_correct))
print('Micro Percentage: ' + str(micro_correct/micro_total*100))

# Total: 81639614
# Correct: 80925959
# Wrong: 713655
# Percentage: 99.12584716532345
# Micro Total: 11232438
# Micro Correct: 10615323
# Micro Percentage: 94.50595676557485
