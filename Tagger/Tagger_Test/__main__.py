# --------------------------------
# Tagger Tester
# Made by Jacob Schnoor
# 11/17/20
#
# ==What is it?
#
# The Tagger Tester is the second of a three part program to tag parts of speech. For more information on the general
# program, see the Tagger Trainer.
#
#
# The Tagger Tester specifically serves the role of assigning tags to a test set of unlabeled words. It does this by
# referencing the probability list and comparing those words to the words in the test set. Anything that is not found
# in the probability list requires the program to more or less just guess the tag. By assigning tags to an unlabeled
# set, we can later compare the program's responses to an answer key and get an idea of its accuracy.
#
# ==How do I use it?
#
# The Tagger Tester runs in Python off the commandline with the following format:
#
# 	python Tagger_Test mode probability_list.txt test.txt test-mode.txt
#
# Where mode is either 0 or 1 (mode 0 is baseline, mode 1 is more accurate). probability_list.txt is a well
# formatted, sorted list of words, tags, and their respective likelihoods. test.txt is the test set where every line
# is a single word. test-mode.txt is the name of the output file that will later be graded by Tagger Evaluator.
#
# For example, one may type:
#
# 	python Tagger_Test 0 tagger-train-prob.txt pos-test.txt pos-test-0.txt
#
# And get the following output in pos-test-0.txt:
#
# No/DT
# ,/,
# it/PRP
# was/VBD
# n't/RB
# Black/NNP
# Monday/NNP
# ./.
# But/CC
# while/IN
#    .
#    .
#    .
# in/IN
# Europe/NNP
# Friday/NNP
# ./.
#
# (File is about 57,000 lines long)
#
# ==How does it work?
#
# The Tagger Tester is broken up into a few pieces (more details follow in the code):
#
# 	1) Initialize variables, introduce user, and open files
# 	2) Set the word tag equal to the most likely tag for that word from the probability list, if possible
# 	3) [Mode 0]: If not possible, just call it a noun
# 	4) [Mode 1]: If not possible, correct using A-rules
# 	5) [Mode 1]: If the word was found, double check it with B-rules
# 	6) Write the words with their tags appended on in the output file
# 	7) Indicate completion

import sys


# 4) A - Rules for guessing at unseen words in Mode 1. Rules are explained below
def correct_unknown(word, previous_tag):
    # A-1 : If the unseen word is preceded by a token of type "TO" it is determined to be a verb
    # Example: "I like TO RUN" guesses that "RUN" is a verb
    if previous_tag == "TO":
        return "VB"
    if word[:1].isupper():
        # A-2
        if word[-1:] == "s":
            return "NNPS"
        # A-3
        else:
            return "NNP"
    else:
        # A-4
        if word[-1:] == "s":
            return "NNS"
        # A-5
        else:
            return "NN"


# B - Rules
def correct_known(word, current_tag, previous_tag):
    if current_tag == "VBD":
        # B-1
        # B-2
        # B-3
        if previous_tag == "VB" or previous_tag == "VBD" or previous_tag == "VBN":
            return "VBN"
    elif current_tag == "VBN":
        # B-4
        # B-5
        # B-6
        # B-7
        if previous_tag == "NN" or previous_tag == "NNP" or previous_tag == "NNS" or previous_tag == "NNPS":
            return "VBD"
    elif current_tag == "VBP":
        # B-8
        if previous_tag == "TO":
            return "VB"
    elif current_tag == "VB":
        # B-9
        # B-10
        # B-11
        # B-12
        if previous_tag == "NN" or previous_tag == "NNP" or previous_tag == "NNS" or previous_tag == "NNPS":
            return "VBP"
    return current_tag


def main(argv):
    # 1) Splits user arguments into all the specified variables
    mode = int(argv[0])
    probability_listname = argv[1]
    test_filename = argv[2]
    output_filename = argv[3]

    # 1) Introduces the user
    print("\nPOS Tagger Tester. CS4242. Made by Jacob Schnoor\n")
    print("Mode:            \t" + str(mode))
    print("Probability List:\t" + probability_listname)
    print("Test File:       \t" + test_filename)
    print("Output File:     \t" + output_filename + "\n")

    # 1) Opens files and sets a default tag of "NN" for singular noun
    test_file = open(test_filename, encoding="utf8")
    out = open(output_filename, "w")
    tag = "NN"
    # 2) Goes line by line in the test_file, checks if that word is anywhere to be found in the probability list.
    # If so, it assigns the word the most likely tag
    for line in test_file:
        probability_list = open(probability_listname, encoding="utf8")
        previous_tag = tag
        # 3) Tag is initially set to "NN" until it's changed by something later on. If it's never changed, then it just
        # stays as a noun
        tag = "NN"
        has_found = False
        next_line = probability_list.readline()
        while not has_found and next_line != "":
            prob_line_split = next_line.split()
            if prob_line_split[0] == line[:-1]:
                has_found = True
                tag = prob_line_split[1]
            next_line = probability_list.readline()
        # Mode 1 for improved accuracy
        if mode == 1:
            # 5) If a word was found in the probability list, double check its veracity with B-rules
            if has_found:
                tag = correct_known(line[:-1], tag, previous_tag)
            # 4) If nothing was found in the original probability list, guess the type using A-rules
            else:
                tag = correct_unknown(line[:-1], previous_tag)
        # 6) Writes the word tag pair to the output file
        out.write(line[:-1] + "/" + tag + "\n")
    # 7) Indicates completion
    print("DONE")


if __name__ == "__main__":
    main(sys.argv[1:])
