# Trainer Program
import re
import sys
from collections import Counter
from itertools import islice

word_tag_pairs = Counter([])
word_counter = Counter([])
word_tag_probs = dict()


def main(argv):
    input_filename = argv[0]
    output_filename = argv[1]

    print("\nPOS Tagger Trainer. CS4242. Made by Jacob Schnoor\n")
    print("Training data:    \t" + input_filename)
    print("Probability file: \t" + output_filename + "\n")

    r_split = re.split(r"(.*)(?<!\\)\/(.*)", open(input_filename, encoding="utf8").read())

    word_counter.update(islice(r_split, 1, None, 3))
    word_tag_pairs.update(zip(islice(r_split, 1, None, 3),
                              islice(r_split, 2, None, 3)))

    # Need to make probability dictionary----------------------------------------------------------------......???
    # for x in word_tag_pairs:

    # out = open(output_filename, "w")
    # for word, word_count in word_counter.most_common():
    #     for (pair_word, tag), pair_count in word_tag_pairs.most_common():
    #         if pair_word == word:
    #             out.write("{:15s}\t{:5s}\t{:8f}\n".format(word, tag, pair_count / word_count))
    # out.close()


if __name__ == "__main__":
    main(sys.argv[1:])
