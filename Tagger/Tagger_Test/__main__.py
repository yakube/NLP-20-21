# Tester Program
import glob
import os
import re
import sys
from collections import Counter
from itertools import islice
from math import sqrt, log


def main(argv):
    input_filename = argv[0]
    output_filename = argv[1]

    print("\nPOS Tagger Tester. CS4242. Made by Jacob Schnoor\n")
    print("Input File:    \t" + input_filename)
    print("Output File: \t" + output_filename + "\n")

    f = open(input_filename, encoding="utf8")


if __name__ == "__main__":
    main(sys.argv[1:])