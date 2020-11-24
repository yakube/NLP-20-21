import sys


def main(argv):
    guess_name = argv[0]
    gold_name = argv[1]
    output_name = argv[2]

    print("\nMachine Grader. CS4242. Made by Jacob Schnoor\n")
    print("System Answers:\t" + guess_name)
    print("Gold Answers:  \t" + gold_name)
    print("Output File:   \t" + output_name + "\n")

    guesses = open(argv[0], encoding="utf8").readlines()
    gold = open(argv[1], encoding="utf8").readlines()
    comparison_str = ""
    total = 0
    correct = 0
    for i in range(len(gold)):
        incorrect = 0
        comparison_str = comparison_str + gold[i][:-1] + " | " + guesses[i][:-1] + " | "
        gold_split = gold[i][:-1].split()
        guess_split = guesses[i][:-1].split()
        total = total + 4
        for j in range(len(gold_split)):
            if gold_split[j] == guess_split[j]:
                correct = correct + 1
            else:
                incorrect = incorrect + 1
        comparison_str = comparison_str + str(incorrect) + "\n"

    out = open(output_name, "w")
    out.write("-----\nAccuracy of " + guess_name + "\n\n" + str(correct / total) + "\n-----\n\n")
    out.write(comparison_str)
    print("DONE")


if __name__ == "__main__":
    main(sys.argv[1:])
