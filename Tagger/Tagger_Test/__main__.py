# Tester Program
import glob
import os
import re
import sys
from collections import Counter
from itertools import islice
from math import sqrt, log


def main(argv):
    mode = argv[0]
    probability_listname = argv[1]
    test_filename = argv[2]
    output_filename = argv[3]

    print("\nPOS Tagger Tester. CS4242. Made by Jacob Schnoor\n")
    print("Mode:            \t" + mode)
    print("Probability List:\t" + probability_listname)
    print("Test File:       \t" + test_filename)
    print("Output File:     \t" + output_filename + "\n")

    test_file = open(test_filename, encoding="utf8")
    out = open(output_filename, "w")
    if mode == str(0):
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
            out.write(line[:-1] + "/" + tag + "\n")
    else:
        print("Mode 1 in progress...")
    print("DONE")


if __name__ == "__main__":
    main(sys.argv[1:])
