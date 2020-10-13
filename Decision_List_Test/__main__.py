# Testing Program
import sys


def main(argv):
    decision_list_name = argv[0]
    test_file_name = argv[1]
    output_file_name = argv[2]

    print("\nDecision List Tester. CS4242. Made by Jacob Schnoor\n")
    print("Decision List :\t\t" + decision_list_name)
    print("Test File :\t\t" + test_file_name)
    print("Output File :\t\t" + output_file_name + "\n")

    decision_file = open(decision_list_name, encoding='utf8')
    test_file = open(test_file_name, encoding='utf8')

    decision_file.close()
    test_file.close()


if __name__ == "__main__":
    main(sys.argv[1:])
