import glob
import os
import re
import sys


def main(argv):
    window_size = int(argv[0])
    corpus_folder_name = argv[1]
    test_pairs_name = argv[2]

    print("\nSimilar to a Point. CS4242. Made by Jacob Schnoor\n")
    print("Window Size:    \t" + str(window_size))
    print("Corpus Folder:  \t" + corpus_folder_name)
    print("Test Pairs File:\t" + test_pairs_name + "\n")

    os.chdir(corpus_folder_name)
    for file_name in glob.glob("*.txt"):
        file = open(file_name, encoding='utf8')
        for line in file:
            words = re.sub(r"[^[a-z0-9\s]", "", line, 0, re.IGNORECASE).lower().split()
            print(words)


if __name__ == "__main__":
    main(sys.argv[1:])
