# python Machine_Reader 0 Machine_Reader\PA6-MCTest\Train\mc500.train.tsv test.0.answers.txt
# exactly 23 elements per row. First couple things are information, etc.
import csv
import sys
import re

# r_p = r"[ .?,!]|(\\newline)"
r_p = r"[ ,.!?]|(\\newline)"
r_t = r"((?:one:)|(?:multiple:))\s(.*)"


def fn(element):
    return not (not element or element == "\\newline")


def ap_arr(question, option):
    apa = re.split(r_p, (re.sub(r_t, "\\2", question) + "" + option).lower())
    apa = list(filter(fn, apa))
    return apa


def max_percent_shared(str_list, apa):
    super_list = []
    for x in range(len(apa)):
        super_list.append(str_list[x:])
    zippy = zip(*super_list)
    max_num = 0
    for z in zippy:
        # print(str(z))
        max_num = max(max_num, len(set(apa).intersection(z)))
    return max_num


def window_slide(story, question, option_a, option_b, option_c, option_d):
    apa_a = ap_arr(question, option_a)
    apa_b = ap_arr(question, option_b)
    apa_c = ap_arr(question, option_c)
    apa_d = ap_arr(question, option_d)

    str_list = list(filter(fn, re.split(r_p, story.lower())))
    # print("\n\n" + str(str_list))
    # print("-----\n" + str(len(apa_a)) + "\n----")
    a_percent = max_percent_shared(str_list, apa_a)
    b_percent = max_percent_shared(str_list, apa_b)
    c_percent = max_percent_shared(str_list, apa_c)
    d_percent = max_percent_shared(str_list, apa_d)

    b_m_p = max(a_percent, b_percent, c_percent, d_percent)

    if b_m_p == a_percent:
        return "A"
    elif b_m_p == b_percent:
        return "B"
    elif b_m_p == c_percent:
        return "C"
    else:
        return "D"


def main(argv):
    mode = int(argv[0])
    tsv_name = argv[1]
    output_name = argv[2]

    print("\nMachine Reader. CS4242. Made by Jacob Schnoor\n")
    print("Mode:       \t" + str(mode))
    print("TSV File:   \t" + tsv_name)
    print("Output File:\t" + output_name + "\n")

    out = open(output_name, "w")

    tsv = csv.reader(open(tsv_name), delimiter="\t")
    for row in tsv:
        q1 = window_slide(row[2], row[3], row[4], row[5], row[6], row[7])
        q2 = window_slide(row[2], row[8], row[9], row[10], row[11], row[12])
        q3 = window_slide(row[2], row[13], row[14], row[15], row[16], row[17])
        q4 = window_slide(row[2], row[18], row[19], row[20], row[21], row[22])
        out.write(q1 + "\t" + q2 + "\t" + q3 + "\t" + q4 + "\n")

    print("DONE")


if __name__ == "__main__":
    main(sys.argv[1:])
