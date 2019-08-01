import jieba

input_filename = "./datasets/LCSTS/train.txt"
output1_filename = "./datasets/LCSTS/summary_jieba_tok.txt"
output2_filename = "./datasets/LCSTS/text_jieba_tok.txt"

input_file = open(input_filename, "r+")
output1_file = open(output1_filename, "a+")
output2_file = open(output2_filename, "a+")

summary = ""
summary_line = True
count = 0
errorFlag = False

for line in input_file:
    print(count)
    line = line.rstrip()

    try:
        seg_list = jieba.cut(line, cut_all=False)
        string = " ".join(seg_list)

        if summary_line:
            summary = string
        else:
            print("ready")
            if not errorFlag:
                print("write")
                output1_file.write(summary)
                output1_file.write("\n")
                output2_file.write(string)
                output2_file.write("\n")
    except:
        print('Error. Skip.')
        errorFlag = True

    summary_line = not summary_line

    count = count + 1

    if not summary_line:
        errorFlag = False

output1_file.close()
output2_file.close()
