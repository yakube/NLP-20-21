# Evaluator Program
import glob
import os
import re
import sys
from collections import Counter
from itertools import islice
from math import sqrt, log

confusion = Counter([])
equivocated = Counter([])


def main(argv):
    key_name = argv[0]
    test_name = argv[1]
    output_filename = argv[2]

    print("\nPOS Tagger Evaluator. CS4242. Made by Jacob Schnoor\n")
    print("Answer Key: \t" + key_name)
    print("Test File:  \t" + test_name)
    print("Output File:\t" + output_filename + "\n")

    key_lines = open(key_name, encoding="utf8").readlines()
    test_lines = open(test_name, encoding="utf8").readlines()

    correct_identifications = 0
    for i in range(len(key_lines)):
        key_split = re.split(r"(.*)(?<!\\)\/(.*)", key_lines[i])
        test_split = re.split(r"(.*)(?<!\\)\/(.*)", test_lines[i])
        confusion[(test_split[2], key_split[2])] += 1
        if test_split[2] == key_split[2]:
            correct_identifications = correct_identifications + 1
        else:
            equivocated[(test_split[2], key_split[2])] += 1

    out = open(output_filename, "w")

    out.write("-----------------\n")
    out.write(test_name + "\n")
    out.write("Accuracy = " + str(100 * correct_identifications / sum(confusion.values()))[:5] + "%\n")
    out.write("-----------------\n\n")

    for x in sorted(confusion, key=lambda y: (y[0], y[1])):
        out.write("{:4s}\t{:4s}\t{:<15n}\n".format(x[0], x[1], confusion[x]))

    out.write("\n\n\nFrequently Mistaken Tags\n------------------------\n")
    for x in sorted(equivocated, key=lambda y: (-equivocated[y], y[0], y[1]))[:10]:
        out.write("{:4s}\t{:4s}\t{:<15n}\n".format(x[0], x[1], equivocated[x]))

    print("DONE")


if __name__ == "__main__":
    main(sys.argv[1:])
