# Trainer Program
import re
import sys
from collections import Counter
from itertools import islice

word_tag_pairs = Counter([])
word_counter = Counter([])
tag_counter = Counter([])
word_tag_probs = dict()


def main(argv):
    input_filename = argv[0]
    output_filename = argv[1]

    print("\nPOS Tagger Trainer. CS4242. Made by Jacob Schnoor\n")
    print("Training data:    \t" + input_filename)
    print("Probability file: \t" + output_filename + "\n")

    r_split = re.split(r"(.*)(?<!\\)\/(.*)", open(input_filename, encoding="utf8").read())

    word_counter.update(islice(r_split, 1, None, 3))
    tag_counter.update(islice(r_split, 2, None, 3))
    word_tag_pairs.update(zip(islice(r_split, 1, None, 3),
                              islice(r_split, 2, None, 3)))

    out = open(output_filename, "w")
    for word, tag in word_tag_pairs:
        word_tag_probs[(word, tag)] = (word_tag_pairs[(word, tag)] + 1) / (word_counter[word] + len(tag_counter))

    # for x in sorted(word_tag_probs.items(), key=lambda y: y[1], reverse=True):
    for x in sorted(word_tag_probs, key=lambda y: (-word_tag_probs[y], y)):
        out.write("{:30s}\t{:5s}\t{:8f}\n".format(x[0], x[1], word_tag_probs[x]))
        # print(x)
    out.close()
    print("DONE")


if __name__ == "__main__":
    main(sys.argv[1:])
