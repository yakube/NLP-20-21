# Evaluation Program
import sys


def main(argv):
    gold_file_name = argv[0]
    system_answer_name = argv[1]
    output_file_name = argv[2]

    print("\nDecision List Evaluator. CS4242. Made by Jacob Schnoor\n")
    print("Gold File :\t\t" + gold_file_name)
    print("System Answer File :\t" + system_answer_name)
    print("Output File :\t\t" + output_file_name + "\n")

    gold_lines = open(gold_file_name, encoding='utf8').readlines()
    system_answer_lines = open(system_answer_name, encoding='utf8').readlines()
    output_file = open(output_file_name, "w")

    t_n = 0
    t_p = 0
    f_n = 0
    f_p = 0

    for i in range(len(gold_lines)):
        split_line = gold_lines[i].split()
        system_answer = int(system_answer_lines[i].split()[1])

        if int(split_line[1]) == system_answer:
            # True Negative
            if int(split_line[1]) == 0:
                t_n = t_n + 1

            # True Positive
            else:
                t_p = t_p + 1

            output_file.write(split_line[0] + " " + split_line[1] + " " + str(system_answer) + "\n")
        else:
            # False Negative
            if int(split_line[1]) == 1:
                f_n = f_n + 1

            # False Positive
            else:
                f_p = f_p + 1

            output_file.write(split_line[0] + " " + split_line[1] + " " + str(system_answer) + " X\n")

    output_file.write("\nStats\n------------------\n")
    output_file.write("Accuracy\t" + str(100 * ((t_p + t_n) / (t_p + t_n + f_p + f_n)))[:4] + "%\n")
    output_file.write("Precision\t" + str(100 * (t_p / (t_p + f_p)))[:4] + "%\n")
    output_file.write("Recall\t\t" + str(100 * (t_p / (t_p + f_n)))[:4] + "%\n")
    output_file.close()
    print("PROCESS COMPLETE")

if __name__ == "__main__":
    main(sys.argv[1:])
