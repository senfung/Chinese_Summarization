
# coding: utf-8

# In[1]:


import kenlm
import jieba


# In[2]:


def s2t_dict():
    s2t = dict()
    infile = open("STCharacters.txt","r+",encoding='utf-8')

    for line in infile:
        line = line.rstrip()
        chars = line.split()
        sim = chars[0]
        trads = chars[1:]
        s2t[sim] = trads
    return s2t


# In[3]:


def convert(sentence):
    
    converted = ""

    char_list = sentence.split()
    s2t = s2t_dict()
    
    for char in char_list:
        if char in s2t:
            if len(s2t[char]) > 1:
                max_score = -1000
                max_candidate = ""
                for candidate in s2t[char]:
                    current_sentence =  "".join(list(converted+candidate))
                    score = model.score(current_sentence)
                    # print(converted+candidate, score)
                    if score > max_score:
                        max_score = score
                        max_candidate = candidate
                converted+=max_candidate
            else:
                converted+=s2t[char][0]
        else:
            converted+=char

    return converted


# In[4]:


infile = open("conversions.txt", "r+", encoding="utf-8")

con_dict = dict()

for line in infile:
    line = line.rstrip()
    arr = line.split()
    trad = arr[0]
    sim = arr[1]
    if sim not in con_dict:
        con_dict[sim] = [trad]
    else:
        con_dict[sim].append(trad)
con_dict['-'] = ['-']

checklist = []
for key in con_dict:
    if len(con_dict[key]) > 1:
        for t in con_dict[key]:
            checklist.append(t)


# In[5]:


LM = 'chinese_5gram.arpa'
model = kenlm.Model(LM)

sim_file = open('simplified100.txt', "r+", encoding="utf-8")
tra_file = open('traditional100.txt', "r+", encoding="utf-8")


# In[6]:


total = 0
correct = 0
wrong = 0
micro_total = 0
micro_correct = 0

line_count = 0

tra_lines = tra_file.readlines()

for line in sim_file:
    line = line.rstrip()
    words = list(jieba.cut(line, cut_all = False))
    
    converted_line = ""
    for word in words:
        word_list = list(word)
        word = " ".join(word_list)
        converted = convert(word)
        converted_line = converted_line + converted
        
    line = converted_line
        
    tra_line = tra_lines[line_count].rstrip()
    s = "".join(tra_line.split())
    tra_line = s
    
    print(line)
    print(tra_line)

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
    print(line_count)
    if total > 1:
        print('Percentage: ' + str(correct/total*100))
    if micro_total > 1:
        print('Micro Percentage: ' + str(micro_correct/micro_total*100))

    line_count = line_count + 1

print('Total: ' + str(total))
print('Correct: ' + str(correct))
print('Wrong: ' + str(wrong))

print('Percentage: ' + str(correct/total*100))


# In[7]:


print('Total: ' + str(total))
print('Correct: ' + str(correct))
print('Wrong: ' + str(wrong))
print('Percentage: ' + str(correct/total*100))
print('Micro Total: ' + str(micro_total))
print('Micro Correct: ' + str(micro_correct))
print('Micro Percentage: ' + str(micro_correct/micro_total*100))
    


# In[9]:


# Total: 7863207
# Correct: 7754945
# Wrong: 108262
# Percentage: 98.62318262764798

