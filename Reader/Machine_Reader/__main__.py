# python Machine_Reader 0 PA6-MCTest\Train\mc500.train.tsv train.0.answers.txt
# exactly 23 elements per row. First couple things are information, etc.
import csv
import sys
import re
import spacy

r_p = r"[ ,.!?]|(\\newline)"
r_t = r"((?:one:)|(?:multiple:))\s(.*)"

nlp = spacy.load('en_core_web_sm')


def fn(element):
    return not (not element or element == "\\newline")


def ap_arr(question, option, mode):
    if mode == 1:
        apa = []
        testify = nlp(re.sub(r_t, "\\2", question[:-1] + " " + option))
        ent_dict = {}
        for ent in testify.ents:
            ent_dict[ent.text] = ent.label_
        for token in testify:
            if token.pos_ != 'SPACE':
                apa.append((token.text.lower(), token.pos_, ent_dict.get(token.text)))

    else:
        apa = re.split(r_p, (re.sub(r_t, "\\2", question) + "" + option).lower())
        apa = list(filter(fn, apa))

    return apa


def max_percent_shared(str_list, apa, mode):
    super_list = []
    for x in range(len(apa)):
        super_list.append(str_list[x:])
    zippy = zip(*super_list)
    max_num = 0

    if mode == 1:
        for z in zippy:
            z_text = []

            for x in z:
                z_text.append(x[0])

            apa_text = []
            apa_pos = []
            apa_ent = []
            for x in apa:
                apa_text.append(x[0])
                apa_pos.append(x[1])
                apa_ent.append(x[2])

            weight = 0
            intersect = set(apa_text).intersection(z_text)
            for x in intersect:
                for i in range(len(apa_text)):
                    if x == apa_text[i]:
                        if apa_pos[i] != 'DET' and apa_pos != 'PUNCT':
                            weight = weight + 1

                        if apa_ent[i] is not None:
                            if apa[0][0] == 'who' and apa_ent[i] == 'PERSON':
                                weight = weight + 2
                            elif apa[0][0] == 'where' and apa_ent[i] == 'LOC':
                                weight = weight + 2
                            elif apa[0][0] == 'where' and apa_ent[i] == 'GPE':
                                weight = weight + 2
                            elif apa[0][0] == 'when' and apa_ent[i] == 'TIME':
                                weight = weight + 2
                            elif apa[0][0] == 'when' and apa_ent[i] == 'DATE':
                                weight = weight + 2
            max_num = max(max_num, len(intersect) + weight)

    else:
        for z in zippy:
            max_num = max(max_num, len(set(apa).intersection(z)))

    return max_num


def window_slide(story, question, option_a, option_b, option_c, option_d, mode):
    apa_a = ap_arr(question, option_a, mode)
    apa_b = ap_arr(question, option_b, mode)
    apa_c = ap_arr(question, option_c, mode)
    apa_d = ap_arr(question, option_d, mode)

    if mode == 1:
        str_list = []
        testify = nlp(re.sub(r_p, " ", story))
        ent_dict = {}
        for ent in testify.ents:
            ent_dict[ent.text] = ent.label_
        for token in testify:
            if token.pos_ != 'SPACE':
                str_list.append((token.text.lower(), token.pos_, ent_dict.get(token.text)))
    else:
        str_list = list(filter(fn, re.split(r_p, story.lower())))
    a_percent = max_percent_shared(str_list, apa_a, mode)
    b_percent = max_percent_shared(str_list, apa_b, mode)
    c_percent = max_percent_shared(str_list, apa_c, mode)
    d_percent = max_percent_shared(str_list, apa_d, mode)

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
        q1 = window_slide(row[2], row[3], row[4], row[5], row[6], row[7], mode)
        q2 = window_slide(row[2], row[8], row[9], row[10], row[11], row[12], mode)
        q3 = window_slide(row[2], row[13], row[14], row[15], row[16], row[17], mode)
        q4 = window_slide(row[2], row[18], row[19], row[20], row[21], row[22], mode)
        out.write(q1 + "\t" + q2 + "\t" + q3 + "\t" + q4 + "\n")

    print("DONE")


if __name__ == "__main__":
    main(sys.argv[1:])
