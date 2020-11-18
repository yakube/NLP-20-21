# python Machine_Reader 0 Machine_Reader\PA6-MCTest\Train\mc500.train.tsv test.0.answers.txt
# exactly 23 elements per row. First couple things are information, etc.
import csv
import sys


def main(argv):
    mode = int(argv[0])
    tsv_name = argv[1]
    output_name = argv[2]

    print("\nMachine Reader. CS4242. Made by Jacob Schnoor\n")
    print("Mode:       \t" + str(mode))
    print("TSV File:   \t" + tsv_name)
    print("Output File:\t" + output_name + "\n")

    tsv = csv.reader(open(tsv_name), delimiter="\t")
    for row in tsv:
        print(row[0])


if __name__ == "__main__":
    main(sys.argv[1:])
