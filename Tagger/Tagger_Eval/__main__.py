# --------------------------------
# Tagger Evaluator
# Made by Jacob Schnoor
# 11/17/20
#
# ==What is it?
#
# The Tagger Evaluator is the third of a three part program that seeks to perform accurate part-of-speech tagging.
# For more information on the general program, see Tagger Tester and Tagger Trainer.
#
# The Tagger Evaluator specifically serves as the automated grader for the part of speech tagger. It looks at the
# guesses for tags that Tagger Tester provided and cross references them with the answer sheet. In addition to pure
# accuracy, the evaluator also gives a number of statistics corresponding to a confusion matrix. Basically,
# it prints out all nonzero guess/answer pairs in a human readable format. It also has a section at the bottom where
# it lists the most frequently messed up guess/answer pairs.
#
# ==How do I use it?
#
# The Tagger Evaluator runs in Python off the commandline in the following format:
#
# 	python Tagger_Eval answer_key.txt test-mode.txt test-mode-eval.txt
#
# Where answer_key.txt is the answer key with the correct identifications for word tags. test-mode.txt is the test
# file from Tagger Tester. test-mode-eval.txt is the output file that will have statistics about the Tagger's
# accuracy and confused identifications
#
# For example, the following command:
#
# 	python Tagger_Eval pos-key.txt pos-test-0.txt pos-test-0-eval.txt
#
# Results in the following being printed in the output file:
#
# -----------------
# pos-test-0.txt
# Accuracy = 92.14%
# -----------------
#
# #   	#   	5
# $   	$   	375
# ''  	''  	528
# (   	(   	76
# )   	)   	76
# ,   	,   	3070
# .   	.   	2363
# :   	:   	336
# CC  	CC  	1361
# CC  	IN  	2
# CC  	NN  	3
#
#    .
#    .
#    .
# Frequently Mistaken Tags
# ------------------------
# NN  	NNP 	512
# NN  	JJ  	319
# NN  	VB  	262
# VBD 	VBN 	233
#    .
#    .
#    .
#
# (The file is about 180 lines long)
#
# ==How does it work?
#
# The Tagger Evaluator can be broken into a few parts (more details in the code below):
#
# 	1) Initialize variables, open files, and introduce user
# 	2) Classify identifications
# 	3) Print confusion matrix to file
# 	4) Print equivocations to file
# 	5) Indicate completion

import re
import sys
from collections import Counter

confusion = Counter([])
equivocated = Counter([])


def main(argv):
    # 1) Splits user arguments into variables
    key_name = argv[0]
    test_name = argv[1]
    output_filename = argv[2]

    # 1) Introduces the user
    print("\nPOS Tagger Evaluator. CS4242. Made by Jacob Schnoor\n")
    print("Answer Key: \t" + key_name)
    print("Test File:  \t" + test_name)
    print("Output File:\t" + output_filename + "\n")

    # 1) Opens specified files
    key_lines = open(key_name, encoding="utf8").readlines()
    test_lines = open(test_name, encoding="utf8").readlines()

    # 1) Initializes correct_identifications variable for keeping track of accuracy
    correct_identifications = 0
    # 2) For every line in the answer key, split the answer key line into its word and respective tag. Also grab the tag
    # from the test file. Increment the number of occurrences of that test-tag with that answer-tag. If they're the
    # same thing, increment the number of correct_identifications. If not, add that pair to the equivocated matrix
    for i in range(len(key_lines)):
        key_split = re.split(r"(.*)(?<!\\)\/(.*)", key_lines[i])
        test_split = re.split(r"(.*)(?<!\\)\/(.*)", test_lines[i])
        confusion[(test_split[2], key_split[2])] += 1
        if test_split[2] == key_split[2]:
            correct_identifications = correct_identifications + 1
        else:
            equivocated[(test_split[2], key_split[2])] += 1

    # 3) Open the output file for writing
    out = open(output_filename, "w")

    # 3) Some formatting along with an accuracy calculator. It takes correct_identifications as a percentage of the
    # total number of pairs seen.
    out.write("-----------------\n")
    out.write(test_name + "\n")
    out.write("Accuracy = " + str(100 * correct_identifications / sum(confusion.values()))[:5] + "%\n")
    out.write("-----------------\n\n")

    # 3) This prints a sorted confusion matrix to the file. It sorts alphabetically by the test-tag, then alphabetically
    # by the answer-tag. It prints all these value into the file
    for x in sorted(confusion, key=lambda y: (y[0], y[1])):
        out.write("{:4s}\t{:4s}\t{:<15n}\n".format(x[0], x[1], confusion[x]))

    # 4) This prints the equivocations to the file. This time it sorts first by most incorrect, then alphabetically.
    # This is helpful for quickly determining which word pairs are most often mistaken.
    out.write("\n\n\nFrequently Mistaken Tags\n------------------------\n")
    for x in sorted(equivocated, key=lambda y: (-equivocated[y], y[0], y[1]))[:10]:
        out.write("{:4s}\t{:4s}\t{:<15n}\n".format(x[0], x[1], equivocated[x]))

    # 5) The "DONE" indicates that the program has finished running
    print("DONE")


if __name__ == "__main__":
    main(sys.argv[1:])
