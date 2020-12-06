# --------------------------------
# Machine Reader
# Made by Jacob Schnoor
# 12/6/20
#
# ==What is it?
#
# The Machine Reader is a program that is designed to take the MC500, a set of multiple choice questions developed by
# Microsoft to assess reading comprehension. The questions are designed to be at about an elementary aged reading
# level and they are divided into a training, development, and test set where the idea is that software engineers
# would closely study the training data, run several trials on the development data, and ultimately assess their
# final score on the test data.
#
# The rationale behind this separation is that as programmers, we are seeking a generalizable algorithm for
# extracting information, rather than anything that is hyperspecific or overly trained on one piece of data.
#
# The program that I have created here makes heavy use of the "sliding window" baseline which I describe in greater
# detail in the code. Mode 0 is exclusively a sliding window, and mode 1 offers enhancements that include POS
# tagging, named entity recognition, and question type analysis. By doing this, I have created a program that is
# approximately 54.5% accurate at guessing the correct answer (recall that about 25% accuracy can be achieved by
# random guessing).
#
# ==How do I use it?
#
# The Machine Reader runs in python off the command line with the following format
#
# 	python Machine_Reader MODE data.tsv data.MODE.answers.txt
#
# Where MODE is either a 0 or a 1 representing either the sliding window baseline or the baseline with enhancements.
# data.tsv is the tab-separated data where stories, questions, and answers are formatted according to MC500
# guidelines. data.MODE.answers.txt is the output file where the computer writes down all its guesses. These attempts
# will be compared later on in the Machine_Grader portion.
#
# As an example, one might run
#
# 	python Machine_Reader 0 PA6-MCTest\Train\mc500.train.tsv train.0.answers.txt
#
# And get the following output in train.0.answers.txt:
#
#   B	C	A	D
#   B	A	D	A
#   D	A	D	C
#   A	B	C	C
#   D	C	D	A
#   B	C	A	B
#   A	B	A	C
#   D	C	C	A
#   A	B	A	B
#   A	A	C	A
#
# 	    .
# 	    .
# 	    .
#
#   B	A	A	B
#   B	A	B	D
#   D	A	B	D
#
# (The file is approximately 300 lines long)
#
# ==How does it work?
#
# As previously stated, the Machine Reader program relies heavily upon the "sliding window" method. In a general
# sense, one can think of this like the program is gluing together the question with each answer option and sliding
# through the story like it was the opening of a ziploc bag. At every possible step, it merely asks "how many words
# are shared between the question-answer pair and this x-length bloc of the story?" where x is the number of words in
# our question-answer pair.
#
# If we have a story like: "Johnny lived in a mountain and his favorite sport in the world was tennis"
#
# And our question is: "Where does Johnny live?"
# 			A. a mountain
# 			B. Detroit
# 			C. a lake
# 			D. in a tree
#
# Our question-answer pairs are literally
#
# 	where does johnny live a mountain
# 	where does johnny live detroit
# 	where does johnny live a lake
# 	where does johnny live in a tree
#
# And we slide along the story by first looking at:
#
# 	shared_words("where does johnny live a mountain", "johnny lived in a mountain and")
# 	shared_words("where does johnny live a mountain", "lived in a mountain and his")
# 	shared_words("where does johnny live a mountain", "in a mountain and his favorite")
# 	shared_words("where does johnny live a mountain", "a mountain and his favorite sport")
#
# 		.
# 		.
# 		.
#
# 	shared_words("where does johnny live a mountain", "sport in the world was tennis")
#
# For option A, taking note of what our maximum value was along the way. Note that each chunk is 6 words long because
# our question-answer pair has 6 total words.
#
# Then for option B, we look at:
#
# 	shared_words("where does johnny live detroit", "johnny lived in a mountain")
# 	shared_words("where does johnny live detroit", "lived in a mountain and")
# 	shared_words("where does johnny live detroit", "in a mountain and his")
# 	shared_words("where does johnny live detroit", "a mountain and his favorite")
#
# 		.
# 		.
# 		.
#
# 	shared_words("where does johnny live detroit", "in the world was tennis")
#
# Adjusting our window size to 5 words in length and again recording what our maximum value was along the way.
#
# We do the same thing for options C and D, see which answer had the highest maximum number of shared words with any
# part of the story, and select that answer as correct.
#
# This baseline is surprisingly effective, however it can be improved by adjusting for word conjugation,
# question type, and devaluing the importance of sharing words like "the" and "a" and focusing more on names, etc.
#
# This program is largely separated by whether it is in mode 0 or 1. For simplicity's sake, numbers will be used to
# designate program function and the letters "a" and "b" will stand in for mode 0 and mode 1 respectively. Our major
# program functions are as follows (more details are in the code):
#
# 	1. Parse data, introduce the user, and instantiate variables
# 	2. Create all relevant answer-pairs
# 	3. Find the maximum similarity of each answer pair to the story
# 	4. Designate most similar answer as correct
# 	5. Output all answers in appropriately formatted output file
# 	6. Indicate completion
#
import csv
import sys
import re
import spacy

# 1) Instantiates regular expressions. These are used to cleanly filter our data into word arrays without any extra
# garbage
r_p = r"[ ,.!?]|(\\newline)"
r_t = r"((?:one:)|(?:multiple:))\s(.*)"

# 1) Instantiates the SpaCy module for Python. This will be used to identify Part of Speech and Named Entities
nlp = spacy.load('en_core_web_sm')


# 1) Filtering function that we use later on. It removes "\\newline" characters from our story as well as blank
# entries in our array
def fn(element):
    return not (not element or element == "\\newline")


# 2) Function for creating question-answer pairs
def ap_arr(question, option, mode):
    # 2b) In mode 1, we use SpaCy to help us identify all discrete tokens. We filter out punctuation and formatting.
    # We store all tokens as tuples which contain the text itself, the part of speech label, and the type of Named
    # Entity (Person, Location, etc.) if applicable
    if mode == 1:
        apa = []
        testify = nlp(re.sub(r_t, "\\2", question[:-1] + " " + option))
        ent_dict = {}
        for ent in testify.ents:
            ent_dict[ent.text] = ent.label_
        for token in testify:
            if token.pos_ != 'SPACE':
                apa.append((token.text.lower(), token.pos_, ent_dict.get(token.text)))
    # 2a) In mode 0, we simply split the question into lowercase words and filter out punctuation and formatting
    else:
        apa = re.split(r_p, (re.sub(r_t, "\\2", question) + "" + option).lower())
        apa = list(filter(fn, apa))

    return apa


# 3) This function is something of a misnomer. Originally, it was going to look at word sharing as a percentage of the
# overall question_answer pair length, but it was determined through development trials that raw numbers actually tend
# to be more accurate
#
# Regardless, it looks at a list of word arrays from the story that are x-long, compares each with the
# question-answer pair, and returns a maximum value of similarity to the story.
def max_percent_shared(str_list, apa, mode):
    # 3) The function initially using "zipping" to scan through a word array of the story and create all word arrays
    # of length x that will later be used for comparison
    super_list = []
    for x in range(len(apa)):
        super_list.append(str_list[x:])
    zippy = zip(*super_list)
    max_num = 0

    # 3b) In mode 1, comparisons are based off of SpaCy's identifications of lower-cased token text. A moderate amount
    # of weight is added to "important" parts of speech which are anything other than determiners and punctuation. While
    # this is incredibly simplistic, it seemed to help more than it hurt during development trials. Probably because
    # words like "the" are not as useful as nouns or verbs.
    #
    # A heavier amount of weight was also added to common cases where the question type very clearly matched an answer
    # type. This ideally helped to cut down guesses that don't even make semantic sense.
    if mode == 1:
        for z in zippy:
            # 3b) Converts tuples into usable arrays of their respective texts, parts of speech, and entity designators
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

            # 3b) Sets an initial weight of 0 and analyzes the attributes of the shared words. This uses POS Tagging,
            # Named Entity Recognition, and Question Type Analysis.
            weight = 0
            intersect = set(apa_text).intersection(z_text)
            for x in intersect:
                for i in range(len(apa_text)):
                    if x == apa_text[i]:
                        # 3b) If a shared word is a non-determiner and a non-punctuation word (such as adjective, verb,
                        # etc.), it gets a weight of +1 added on. They are deemed to be more important
                        if apa_pos[i] != 'DET' and apa_pos != 'PUNCT':
                            weight = weight + 1

                        # 3b) If a shared word is an entity that obviously fits the criteria of the question
                        # (who -> person, where -> location, etc.), it gets a weight of +2 added on. The weight values
                        # themselves are pretty much arbitrary, but their purpose is to prioritize certain types of
                        # similarity rather than just raw word matching.
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
        # 3a) Mode 0 just returns the maximum word set intersection size along the sliding path. Works exactly as
        # described in the initial comment up top.
        for z in zippy:
            max_num = max(max_num, len(set(apa).intersection(z)))

    return max_num


# 4) This function handles the logistics of calling the question-answer pair creation method, turning our story into a
# word array, and returning whichever answer option was deemed most similar
def window_slide(story, question, option_a, option_b, option_c, option_d, mode):
    # 4) Calls ap_arr to get all question-answer pairs to use for sliding
    apa_a = ap_arr(question, option_a, mode)
    apa_b = ap_arr(question, option_b, mode)
    apa_c = ap_arr(question, option_c, mode)
    apa_d = ap_arr(question, option_d, mode)

    # 4b) Mode 1 uses SpaCy to divide our story into discrete tokens. We save each token as a tuple with its relevant
    # data (lowercase text, POS Tag, Entity Label if applicable)
    if mode == 1:
        str_list = []
        testify = nlp(re.sub(r_p, " ", story))
        ent_dict = {}
        for ent in testify.ents:
            ent_dict[ent.text] = ent.label_
        for token in testify:
            if token.pos_ != 'SPACE':
                str_list.append((token.text.lower(), token.pos_, ent_dict.get(token.text)))

    # 4a) Mode 0 just splits our story by space, puts all words into lowercase, and attempts to filter out garbage by
    # using our regular expression
    else:
        str_list = list(filter(fn, re.split(r_p, story.lower())))

    # 4) We analyze which option yields the highest percentage and designate that as the answer to return. In cases of
    # a tie, the A supersedes B which supersedes C which supersedes D.
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


# The main method
def main(argv):
    # 1) Handles commandline arguments, introduces the user, and instantiates the relevant variables
    mode = int(argv[0])
    tsv_name = argv[1]
    output_name = argv[2]

    print("\nMachine Reader. CS4242. Made by Jacob Schnoor\n")
    print("Mode:       \t" + str(mode))
    print("TSV File:   \t" + tsv_name)
    print("Output File:\t" + output_name + "\n")

    # 5) Scans through the TSV file and for each question, applies either the mode 0 algorithm or the mode 1 algorithm
    # The results are written to the output file in order with four answers per line, separated by tabs
    out = open(output_name, "w")
    tsv = csv.reader(open(tsv_name), delimiter="\t")
    for row in tsv:
        q1 = window_slide(row[2], row[3], row[4], row[5], row[6], row[7], mode)
        q2 = window_slide(row[2], row[8], row[9], row[10], row[11], row[12], mode)
        q3 = window_slide(row[2], row[13], row[14], row[15], row[16], row[17], mode)
        q4 = window_slide(row[2], row[18], row[19], row[20], row[21], row[22], mode)
        out.write(q1 + "\t" + q2 + "\t" + q3 + "\t" + q4 + "\n")

    # 6) The "DONE" statement is printed to the screen indicating that all processing has been completed
    print("DONE")


if __name__ == "__main__":
    main(sys.argv[1:])
