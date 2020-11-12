# Tester Program
import glob
import os
import re
import sys
from collections import Counter
from itertools import islice
from math import sqrt, log


def correct_known(word, previous_tag):
    return previous_tag


def correct_unknown(word):
    print(word)
    print(word[:1])
    if word[:1].isupper():
        return "NNP"
    return "NN"


def main(argv):
    mode = int(argv[0])
    probability_listname = argv[1]
    test_filename = argv[2]
    output_filename = argv[3]

    print("\nPOS Tagger Tester. CS4242. Made by Jacob Schnoor\n")
    print("Mode:            \t" + str(mode))
    print("Probability List:\t" + probability_listname)
    print("Test File:       \t" + test_filename)
    print("Output File:     \t" + output_filename + "\n")

    test_file = open(test_filename, encoding="utf8")
    out = open(output_filename, "w")
    print(test_file)
    for line in test_file:
        probability_list = open(probability_listname, encoding="utf8")
        tag = "NN"
        has_found = False
        next_line = probability_list.readline()
        while not has_found and next_line != "":
            prob_line_split = next_line.split()
            if prob_line_split[0] == line[:-1]:
                has_found = True
                tag = prob_line_split[1]
            next_line = probability_list.readline()
        if mode == 1:
            if has_found:
                tag = correct_known(line[:-1], tag)
            else:
                tag = correct_unknown(line[:-1])
        out.write(line[:-1] + "/" + tag + "\n")
    print("DONE")


if __name__ == "__main__":
    main(sys.argv[1:])
