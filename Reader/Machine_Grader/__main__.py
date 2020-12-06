# --------------------------------
# Machine Grader
# Made by Jacob Schnoor
# 12/6/20
#
# ==What is it?
#
# The Machine Grader is the complementary program to the Machine Reader, which attempts to correctly answer questions
# from the MC500. For more information about the general goals of the reading comprehension task or the MC500,
# look at the Machine Reader.
#
# The Machine Grader specifically is the program that grades the accuracy of the Machine Reader. By taking in a set
# of guesses and looking at the answer key, this program can tell the user how good the Machine Reader is at
# understanding material.
#
# ==How do I use it?
#
# The Machine Grader runs in Python off the commandline with the following format:
#
# 	python Machine_Grader guesses.txt answer_key.ans guesses.graded.txt
#
# Where guesses.txt is the output file from the Machine Reader program. answer_key.ans is the set of correct answers
# for the data. guesses.graded.txt will be the output file that will tell the user how well the program did.
#
# As an example, one might type:
#
# 	python Machine_Grader train.0.answers.txt PA6-MCTest\Train\mc500.train.ans train.0.graded.txt
#
# And get the following output in train.0.graded.txt:
#
# -----
# Accuracy of train.0.answers.txt
#
# 0.5416666666666666
# -----
#
# B	C	C	D | B	C	A	D | 1
# B	D	D	B | B	A	D	A | 2
# D	D	D	B | D	A	D	C | 2
# A	B	C	C | A	B	C	C | 0
# C	C	D	A | D	C	D	A | 1
# C	C	A	C | B	C	A	B | 2
# A	B	C	C | A	B	A	C | 1
# 	.
# 	.
# 	.
# C	D	A	B | B	A	A	B | 2
# C	A	B	D | B	A	B	D | 1
# A	D	C	D | D	A	B	D | 3
#
# (File is approximately 300 lines long)
#
# In this output file, correct answers are on the left side, guesses are in the middle, and the number of mistakes is
# on the right. At the top, the decimal represents the correct proportion of answers. So in this case, we got a score
# of 54.167%
#
# ==How does it work?
#
# The grader is a very simple program broken up into a few parts (more details follow in the code):
#
# 	1) Initialize variables and introduce user
# 	2) Read the guesses file and the answer file
# 	3) Count up correct and incorrect answers
# 	4) Report score
# 	5) Display answers side by side
# 	6) Indicate completion
#
import sys


def main(argv):
    # 1) Splits commandline arguments, introduces the user, and opens the relevant files
    guess_name = argv[0]
    gold_name = argv[1]
    output_name = argv[2]

    print("\nMachine Grader. CS4242. Made by Jacob Schnoor\n")
    print("System Answers:\t" + guess_name)
    print("Gold Answers:  \t" + gold_name)
    print("Output File:   \t" + output_name + "\n")

    guesses = open(argv[0], encoding="utf8").readlines()
    gold = open(argv[1], encoding="utf8").readlines()
    comparison_str = ""
    total = 0
    correct = 0
    # 2) For every line in the files, create a side-by-side comparison string along with the number of mistakes. Keep
    # a running tally of accuracy
    for i in range(len(gold)):
        incorrect = 0
        comparison_str = comparison_str + gold[i][:-1] + " | " + guesses[i][:-1] + " | "
        gold_split = gold[i][:-1].split()
        guess_split = guesses[i][:-1].split()
        total = total + 4
        # 3) Designate guesses as either correct or incorrect
        for j in range(len(gold_split)):
            if gold_split[j] == guess_split[j]:
                correct = correct + 1
            else:
                incorrect = incorrect + 1
        comparison_str = comparison_str + str(incorrect) + "\n"

    out = open(output_name, "w")
    # 4) Report the score
    out.write("-----\nAccuracy of " + guess_name + "\n\n" + str(correct / total) + "\n-----\n\n")

    # 5) Write the comparison lines to the file
    out.write(comparison_str)

    # 6) Indicate completion
    print("DONE")


if __name__ == "__main__":
    main(sys.argv[1:])
