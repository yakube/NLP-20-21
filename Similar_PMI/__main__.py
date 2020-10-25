import glob
import os
import re
import sys
from collections import Counter
from itertools import islice

word_pairs = Counter([])
word_counter = Counter([])


def get_coconut(word_1, word_2):
    return word_pairs[tuple((word_1, word_2))] + word_pairs[tuple((word_2, word_1))]


def get_pmi(word_1, word_2, total_tokens):
    prob_1 = word_counter[word_1] / total_tokens
    prob_2 = word_counter[word_2] / total_tokens
    prob_coconut = get_coconut(word_1, word_2) / total_tokens
    if prob_1 == 0 or prob_2 == 0:
        return -999
    else:
        return prob_coconut / (prob_1 * prob_2)


def main(argv):
    window_size = int(argv[0])
    corpus_folder_name = argv[1]
    test_pairs_name = argv[2]

    test_pairs = open(test_pairs_name, encoding='utf8')

    print("\nSimilar to a Point. CS4242. Made by Jacob Schnoor")
    print("Computing similarity from a word by word PMI co-occurrence matrix\n")
    print("Window Size:    \t" + str(window_size))
    print("Corpus Folder:  \t" + corpus_folder_name)
    print("Test Pairs File:\t" + test_pairs_name + "\n")

    total_tokens = 0
    os.chdir(corpus_folder_name)
    for file_name in glob.glob("*.txt"):
        file = open(file_name, encoding='utf8')
        for line in file:
            words = re.sub(r"[^[a-z0-9\s]", "", line, 0, re.IGNORECASE).lower().split()
            word_counter.update(words)
            total_tokens = total_tokens + len(words)
            for x in range(1, window_size):
                # print(list(zip(words, islice(words, x, None))))
                word_pairs.update(zip(words, islice(words, x, None)))

    print("Tokens =\t\t" + str(total_tokens))
    print("Types = \t\t" + str(len(word_counter)) + "\n")

    header = '{0:15s} {1:15s} {2:15s} {3:15s} {4:15s} {5:15s}'
    template = '{0:15s} {1:15s} {2:<15d} {3:<15d} {4:<15d} {5:<15f}'

    print(header.format("Word 1", "Word 2", "Word 1 Count", "Word 2 Count", "Co-Count", "PMI"))
    print(header.format("------", "------", "------------", "------------", "--------", "---"))

    for line in test_pairs:
        split_line = line.split()
        word_1 = split_line[0]
        word_2 = split_line[1]

        print(template.format(word_1, word_2, word_counter[word_1], word_counter[word_2], get_coconut(word_1, word_2),
                              get_pmi(word_1, word_2, total_tokens)))


if __name__ == "__main__":
    main(sys.argv[1:])
