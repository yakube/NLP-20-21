# --------------------------------
# Decision List Evaluator
# Made by Jacob Schnoor
# 10/22/20
#
# ==What is it?
#
# The Decision List Evaluator is the third of a three part program that seeks to classify movie review sentiment by
# the text content of the review. The Evaluator is the part that takes system guesses and writes them to the right of
# the master copy. Essentially it is "grading" the Decision List's competence by looking at how many reviews it
# guesses correctly, and how many it doesn't. For more information on the general goals of this program,
# see Decision_List_Train and Decision_List_Test.
#
# ==How do I use it?
#
# The Decision List Evaluator runs in Python off the commandline with the following format:
#
# 	python Decision_List_Eval gold_file.txt system_answers.txt output_file.txt
#
# Where gold_file.txt contains the review names with the correct answers, system_answers.txt is the output of
# Decision_List_Test, and output_file.txt will contain the graded report.
#
# ==How does it work?
#
# As mentioned previously, the Evaluator is just a simple grader made up of a few parts:
#
# 	1) Introduction, variable instantiation, and file opening
# 	2) Line by line assessment
# 	3) Accuracy calculations
# 	4) Writing to file and conclusion
#
# I go into more detail in the code
import sys


def main(argv):
    # 1) Argument splitting
    gold_file_name = argv[0]
    system_answer_name = argv[1]
    output_file_name = argv[2]

    # 1) Introduction and confirmation that arguments were received correctly
    print("\nDecision List Evaluator. CS4242. Made by Jacob Schnoor\n")
    print("Gold File :\t\t" + gold_file_name)
    print("System Answer File :\t" + system_answer_name)
    print("Output File :\t\t" + output_file_name + "\n")

    # 1) File opening
    gold_lines = open(gold_file_name, encoding='utf8').readlines()
    system_answer_lines = open(system_answer_name, encoding='utf8').readlines()
    output_file = open(output_file_name, "w")

    # 1) Instantiating variables for (true and false) (positives and negatives) (4 total variables)
    t_n = 0
    t_p = 0
    f_n = 0
    f_p = 0

    # 2) Go line by line in the "gold answers" document. Split into filename and correct number. Based on that number,
    # compared to the system number, increment true negative, true positive, false negative, or false positive based
    # on the nature of agreement/disagreement
    for i in range(len(gold_lines)):
        split_line = gold_lines[i].split()
        system_answer = int(system_answer_lines[i].split()[1])

        # 2) If the golden answer equals the system answer, then it's a true something
        if int(split_line[1]) == system_answer:
            # True Negative
            if int(split_line[1]) == 0:
                t_n = t_n + 1

            # True Positive
            else:
                t_p = t_p + 1

            # 2) Write filename, golden answer, then system answer (no marking implies that they agree)
            output_file.write(split_line[0] + " " + split_line[1] + " " + str(system_answer) + "\n")
        # 2) If golden answer does NOT equal system answer, then it is a false something
        else:
            # False Negative
            if int(split_line[1]) == 1:
                f_n = f_n + 1

            # False Positive
            else:
                f_p = f_p + 1

            # 2) Write filename, golden answer, system answer, then an "X" indicating disagreement
            output_file.write(split_line[0] + " " + split_line[1] + " " + str(system_answer) + " X\n")

    # 3) and 4) The program calculates accuracy, precision, and recall based on the relationships between true
    # positives, true negatives, etc. then prints those stats at the bottom of the graded report. This gets saved in
    # the output file which the user can go read
    output_file.write("\nStats\n------------------\n")
    output_file.write("Accuracy\t" + str(100 * ((t_p + t_n) / (t_p + t_n + f_p + f_n)))[:4] + "%\n")
    output_file.write("Precision\t" + str(100 * (t_p / (t_p + f_p)))[:4] + "%\n")
    output_file.write("Recall\t\t" + str(100 * (t_p / (t_p + f_n)))[:4] + "%\n")
    output_file.close()

    # 4) Verification that program has completed the process
    print("PROCESS COMPLETE")


if __name__ == "__main__":
    main(sys.argv[1:])
