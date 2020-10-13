# Training Program
# I  am adding text to test git
import math
import sys
from collections import Counter


def main(argv):
    input_name = argv[0]
    output_name = argv[1]

    print("\nDecision List Trainer. CS4242. Made by Jacob Schnoor\n")
    print("Using [" + input_name + "] to make decision tree \nStoring it in [" + output_name + "]...\n")

    f = open(input_name, encoding='utf8')

    # word_array_0 = []
    # word_array_1 = []
    # temp_array = []

    word_0_counter = Counter([])
    word_1_counter = Counter([])
    for line in f:
        split_line = line.split()
        if split_line[1] == str(0):
            word_0_counter.update(split_line[2:])
        elif split_line[1] == str(1):
            word_1_counter.update(split_line[2:])

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
    #     log_ratio = math.log((word_1_counter[x[1]] + 1) / (word_0_counter[x[1]] + 1), 2)
    #     if log_ratio < 0:
    #         value_dictionary[x[0]] = 0
    #     else:
    #         value_dictionary[x[0]] = 1
    #     strength_dictionary[x[0]] = abs(log_ratio)
    #
    strength_dictionary = sorted(strength_dictionary.items(), key=lambda k: k[1], reverse=True)
    for x, count in strength_dictionary[:30]:
        print('%20s\t%3d\t%3f' % (x[:20], value_dictionary[x], count))

    # print('%20s: %3d' % (x[:20], count))

    # temp_array = line.split()
    # if int(temp_array[1]) == 0:
    #     for x in temp_array[2:]:
    #         word_array_0.append(x)
    # elif int(temp_array[1]) == 1:
    #     for x in temp_array[2:]:
    #         word_array_1.append(x)

    # w_log_dictionary = {}
    # # for x in word_array_0:
    # #     if x not in w_log_dictionary:
    # #         # w_log_dictionary[x] = len(x)
    # #         occur_count_0 = 1
    # #         occur_count_1 = 1
    # #         for y in word_array_0:
    # #             if x == y:
    # #                 occur_count_0 = occur_count_0 + 1
    # #         for y in word_array_1:
    # #             if x == y:
    # #                 occur_count_1 = occur_count_1 + 1
    # #         w_log_dictionary[x] = math.log(occur_count_1/occur_count_0, 2)
    #
    # for x in word_array_0[:3000]:
    #     w_log_dictionary[x] = word_array_0.count(x) + word_array_1.count(x)
    #     # if x not in w_log_dictionary:
    #
    #
    # for x in w_log_dictionary:
    #     print(x + "\t" + str(w_log_dictionary[x]))
    # # print("TRAINING COMPLETE")
    #
    # print(len(word_array_0))
    # print(len(word_array_1))
    # for x in word_total_counter:
    #     print('%s : %d' % (x, word_0_counter[x]))
    # print(counts)


if __name__ == "__main__":
    main(sys.argv[1:])
