# Training Program
# I  am adding text to test git
import math
import re
import sys
from collections import Counter
from itertools import islice, zip_longest


def main(argv):
    input_name = argv[0]
    output_name = argv[1]
    not_detector = r"(not)|(can'?t)|(isn'?t)|(couldn'?t)|(didn'?t)|(hadn'?t)|(haven'?t)|(wasn'?t)|(aren'?t)|(\w*n't)"

    print("\nDecision List Trainer. CS4242. Made by Jacob Schnoor\n")
    print("Using [" + input_name + "] to make decision tree \nStoring it in [" + output_name + "]...\n")

    f = open(input_name, encoding='utf8')

    word_0_counter = Counter([])
    word_1_counter = Counter([])
    for line in f:
        split_line = line.split()
        the_n_sandwich = False
        n_corrected = []
        for x in split_line:
            if re.match(r"[,.!?]", x) and the_n_sandwich:
                the_n_sandwich = False
                n_corrected.append(x)
            elif re.match(not_detector, x):
                the_n_sandwich = True
                n_corrected.append(x)
            elif the_n_sandwich:
                n_corrected.append("not_" + x)
            else:
                n_corrected.append(x)
        if n_corrected[1] == str(0):
            word_0_counter.update(n_corrected[2:])
            word_0_counter.update(zip_longest(n_corrected, islice(n_corrected[3:], 1, None)))
        elif n_corrected[1] == str(1):
            word_1_counter.update(n_corrected[2:])
            word_1_counter.update(zip_longest(n_corrected, islice(n_corrected[3:], 1, None)))

    word_total_counter = word_0_counter + word_1_counter
    value_dictionary = {}
    strength_dictionary = {}
    for x, count in word_total_counter.most_common(len(word_total_counter)):
        log_ratio = math.log((word_1_counter[x] + 1) / (word_0_counter[x] + 1), 2)
        if not log_ratio == 0:
            if log_ratio < 0:
                value_dictionary[x] = 0
            else:
                value_dictionary[x] = 1
            strength_dictionary[x] = abs(log_ratio)

    strength_dictionary = sorted(strength_dictionary.items(), key=lambda k: k[1], reverse=True)
    for x, count in strength_dictionary[:25]:
        print('%20s\t%3d\t%3f' % (x[:20], value_dictionary[x], count))


if __name__ == "__main__":
    main(sys.argv[1:])
