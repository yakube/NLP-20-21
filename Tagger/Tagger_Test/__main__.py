import sys


# A - Rules
def correct_unknown(word, previous_tag):
    # A-1
    if previous_tag == "TO":
        return "VB"
    if word[:1].isupper():
        # A-2
        if word[-1:] == "s":
            return "NNPS"
        # A-3
        else:
            return "NNP"
    else:
        # A-4
        if word[-1:] == "s":
            return "NNS"
        # A-5
        else:
            return "NN"


# B - Rules
def correct_known(word, current_tag, previous_tag):
    if current_tag == "VBD":
        # B-1
        # B-2
        # B-3
        if previous_tag == "VB" or previous_tag == "VBD" or previous_tag == "VBN":
            return "VBN"
    elif current_tag == "VBN":
        # B-4
        # B-5
        # B-6
        # B-7
        if previous_tag == "NN" or previous_tag == "NNP" or previous_tag == "NNS" or previous_tag == "NNPS":
            return "VBD"
    elif current_tag == "VBP":
        # B-8
        if previous_tag == "TO":
            return "VB"
    elif current_tag == "VB":
        # B-9
        # B-10
        # B-11
        # B-12
        if previous_tag == "NN" or previous_tag == "NNP" or previous_tag == "NNS" or previous_tag == "NNPS":
            return "VBP"
    return current_tag


def main(argv):
    mode = int(argv[0])
    probability_listname = argv[1]
    test_filename = argv[2]
    output_filename = argv[3]

    print("\nPOS Tagger Tester. CS4242. Made by Jacob Schnoor\n")
    print("Mode:            \t" + str(mode))
    print("Probability List:\t" + probability_listname)
    print("Test File:       \t" + test_filename)
    print("Output File:     \t" + output_filename + "\n")

    test_file = open(test_filename, encoding="utf8")
    out = open(output_filename, "w")
    tag = "NN"
    for line in test_file:
        probability_list = open(probability_listname, encoding="utf8")
        previous_tag = tag
        tag = "NN"
        has_found = False
        next_line = probability_list.readline()
        while not has_found and next_line != "":
            prob_line_split = next_line.split()
            if prob_line_split[0] == line[:-1]:
                has_found = True
                tag = prob_line_split[1]
            next_line = probability_list.readline()
        if mode == 1:
            if has_found:
                tag = correct_known(line[:-1], tag, previous_tag)
            else:
                tag = correct_unknown(line[:-1], previous_tag)
        out.write(line[:-1] + "/" + tag + "\n")
    print("DONE")


if __name__ == "__main__":
    main(sys.argv[1:])
