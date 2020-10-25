# --------------------------------
# Decision List Tester
# Made by Jacob Schnoor
# 10/22/20
#
# ==What is it?
#
# The Decision List Tester is the second of a three part program that seeks to classify movie sentiment using a
# constructed decision list of features. The Tester is the part of the program that takes in a formatted decision
# list (in the form of a .txt file) and guesses a number of unknown classifications based on that list. Based on
# these guesses, we can eventually look at part 3 and determine the accuracy, precision, and recall of our model. For
# more information on the general goals of this program, see Decision_List_Train. To look at accuracy evaluation,
# see Decision_List_Eval.
#
# ==How do I use it?
#
# The Decision List Tester runs in Python and can be launched from the commandline as follows:
#
# 	python Decision_List_Test decision_list.txt test_file.txt output_file.txt
#
# Where decision_list.txt is an appropriately formatted decision list file (ideally generated from
# Decision_List_Train), test_file.txt contains movie reviews with unknown classifications, and output_file.txt will
# be the name of the file containing filenames as well as the programs classifications.
#
# ==How does it work?
#
# The Decision List Tester is made up of a few main parts
#
# 	1) Introduction and file opening
# 	2) Line by Line Splitting
# 	3) Not-Correction
# 	4) Keyword Searching
# 	5) Writing to a file
# 	6) Closing files
#
# I go into more detail in the code
import re
import sys


def main(argv):
    # 1) Argument splitting and basic variable instantiation. The not_detector will be used to detect the word "not"
    decision_list_name = argv[0]
    test_file_name = argv[1]
    output_file_name = argv[2]
    not_detector = r"(not)|(can'?t)|(isn'?t)|(couldn'?t)|(didn'?t)|(hadn'?t)|(haven'?t)|(wasn'?t)|(aren'?t)|(\w*n't)"

    # 1) Introduction to the program just to verify that all files were registered correctly
    print("\nDecision List Tester. CS4242. Made by Jacob Schnoor\n")
    print("Decision List :\t\t" + decision_list_name)
    print("Test File :\t\t" + test_file_name)
    print("Output File :\t\t" + output_file_name + "\n")

    # 1) File opening
    decision_file = open(decision_list_name, encoding='utf8')
    test_file = open(test_file_name, encoding='utf8')
    output_file = open(output_file_name, "w")

    # 2) For every line in the test file (with the unknown reviews), split into individual words, do not-correction,
    # and search for features going down the decision list until you find something. When you find a list word, set the
    # guess as that list word's classifier. Print all the names and guesses to the output file
    for line in test_file:
        # 2) Initial line splitting, variable instantiation, and file opening
        split_line = line.split()
        verdict = -1
        decision_file = open(decision_list_name, encoding='utf8')
        next_line = decision_file.readline()

        # 3) Not correction works almost identically to the one in Decision_List_Train. It appends the prefix "not_"
        # to all words that are "sandwiched" between a not_detector word and a punctuation mark
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

        # 4) On any given line of the test file, the program loops through tons of the decision list entries in order.
        # If a verdict hasn't been made yet and there are still decision list words to check, the program checks the
        # next decision feature, and sees if it can be found anywhere in that line. The if statement handles unigram vs
        # bigram features. If any feature is found in a review, the program sets the designation as that feature's
        # classifier and kicks out of the loop
        while verdict == -1 and next_line != "":
            find_all = re.findall(r"^\s*(\S+)(?: (\S+))? {5,}(\d).*$", next_line)[0]
            word_1 = find_all[0]
            word_2 = find_all[1]
            decision_value = int(find_all[2])
            if len(word_2) == 0 and word_1 in n_corrected[2:]:
                verdict = decision_value
            else:
                for x in range(len(n_corrected)-1):
                    if n_corrected[x] == word_1 and n_corrected[x+1] == word_2:
                        verdict = decision_value

            next_line = decision_file.readline()

        # 5) The program writes whatever verdict it came up with for every single review. If there is nothing
        # conclusive, then the verdicts will likely all be -1 which basically means Null in this context
        output_file.write(n_corrected[0] + " " + str(verdict) + "\n")

    # 6) File closing and basic confirmation that the program didn't crash
    decision_file.close()
    test_file.close()
    output_file.close()
    print("PROCESS COMPLETE")


if __name__ == "__main__":
    main(sys.argv[1:])
