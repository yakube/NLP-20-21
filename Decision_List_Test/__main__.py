# Testing Program
# regex=      r"^\s*(\S+)(?: (\S+))?     (\d).*$"
# use \\1 \\2 \\3 to capture respectively
# if 2 is blank, then it's a unigram
import re
import sys


def main(argv):
    decision_list_name = argv[0]
    test_file_name = argv[1]
    output_file_name = argv[2]
    not_detector = r"(not)|(can'?t)|(isn'?t)|(couldn'?t)|(didn'?t)|(hadn'?t)|(haven'?t)|(wasn'?t)|(aren'?t)|(\w*n't)"

    print("\nDecision List Tester. CS4242. Made by Jacob Schnoor\n")
    print("Decision List :\t\t" + decision_list_name)
    print("Test File :\t\t" + test_file_name)
    print("Output File :\t\t" + output_file_name + "\n")

    decision_file = open(decision_list_name, encoding='utf8')
    test_file = open(test_file_name, encoding='utf8')
    output_file = open(output_file_name, "w")

    for line in test_file:
        split_line = line.split()
        verdict = -1
        decision_file = open(decision_list_name, encoding='utf8')
        next_line = decision_file.readline()

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

        while verdict == -1 and next_line != "":
            find_all = re.findall(r"^\s*(\S+)(?: (\S+))? {5,}(\d).*$", next_line)[0]
            word_1 = find_all[0]
            word_2 = find_all[1]
            decision_value = int(find_all[2])
            # print(word_1 + "\t" + str(len(word_2)) + "\t" + str(decision_value))
            if len(word_2) == 0 and word_1 in n_corrected[2:]:
                verdict = decision_value
            else:
                for x in range(len(n_corrected)-1):
                    if n_corrected[x] == word_1 and n_corrected[x+1] == word_2:
                        verdict = decision_value

            next_line = decision_file.readline()
        # print(n_corrected[0] + " " + str(verdict))
        output_file.write(n_corrected[0] + " " + str(verdict) + "\n")

    decision_file.close()
    test_file.close()
    output_file.close()
    print("PROCESS COMPLETE")


if __name__ == "__main__":
    main(sys.argv[1:])
