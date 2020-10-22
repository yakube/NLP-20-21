# --------------------------------
# Decision List Trainer
# Made by Jacob Schnoor
# 10/20/20
#
# ==What is it?
#
# The Decision List Trainer is the first of a three part program that seeks to analyze the sentiment of movie
# reviews. Often times, when people leave reviews, there is some summarizing statement like "4/5 stars" or "thumbs
# up" that can tell us definitively whether the review was more negative or more positive. By scanning in hundreds of
# these reviews, we can determine what kind of word choice and basic sentence structures are most associated with
# either positive reviews or negative reviews.
#
# This first program just creates the "list of rules" that a later program (Decision_List_Test) will draw from. This
# list takes the structure of a decision list where for any given word, its presence will definitively classify
# something as either positive or negative. Rules with more predictive power are placed at the top. I go into more
# detail later on in the comments.
#
# ==How do I use it?
#
# The Decision List Trainer runs in Python and can be launched from the command line. The exact syntax is as follows:
#
# 	python Decision_List_Train input_filename.txt output_filename.txt
#
# Where the input file is a formatted list of training reviews and the output file will be the name of the resulting
# decision list. For an example, we run:
#
# 	python Decision_List_Train sentiment-train.txt sentiment-decision-list.txt
#
# And get the following preview of our list:
#
# Top 10 Preview
# (0 = negative, 1 = positive)
# ---------------------------------------
#               seagal     0     5.807355
#            gladiator     1     5.000000
#              bateman     1     5.000000
#                leila     1     4.954196
#                0 the     0     4.906891
#              maximus     1     4.906891
#             lebowski     1     4.857981
#              humbert     1     4.807355
#                  0 :     0     4.754888
#              gattaca     1     4.754888
#
# The list is much longer than this, and gets stored in the user specified output file, but this gives us a good idea
# of what it generally looks like. The features are sorted in order of absolute predictive power and given a
# designation of 0 for negative and 1 for positive.
#
# ==How does it work?
#
# The program has a few tasks it needs to accomplish
#
# 	1) Open and read the user designated input file
# 	2) Correct for the existence of words like "not" and "didn't"
# 	3) Mark down the occurrences of every word as either a class 0 or class 1
# 	4) Mark down the occurrences of every bigram as either class 0 or class 1
# 	5) Calculate the smoothed logarithmic ratios of each feature
# 	6) Make a decision whether each word indicates class 0 or class 1
# 	7) Sort the word list by absolute value of the log ratios (magnitude)
# 	8) Print the word list to the output file
# 	9) Print a preview top 10 list to the console
#
# I go into more detail in the relevant sections of the code
import math
import re
import sys
from collections import Counter
from itertools import islice, zip_longest


def main(argv):
    # 1) I break apart the command arguments so the first filename is the input file. The second is the output.
    # I use these names to read from a file and write to a file respectively. Unusable, inaccessible, or unavailable
    # files will return errors. It is assumed the user knows to use formatted .txt files
    input_name = argv[0]
    output_name = argv[1]

    # 2) I establish a regular expression known as the "not detector" this will be used later on to detect "not"
    not_detector = r"(not)|(can'?t)|(isn'?t)|(couldn'?t)|(didn'?t)|(hadn'?t)|(haven'?t)|(wasn'?t)|(aren'?t)|(\w*n't)"

    print("\nDecision List Trainer. CS4242. Made by Jacob Schnoor\n")
    print("Using [" + input_name + "] to make decision tree \nStoring it in [" + output_name + "]...\n")

    # 1) opening the file
    f = open(input_name, encoding='utf8')

    # 3) & 4) Counter objects are incredibly useful for counting the features later on. They are known as "high
    # performance containers" in Python and are extremely efficient at making lists of things with associated counts.
    word_0_counter = Counter([])
    word_1_counter = Counter([])

    # 2) I go line by line in the input file, splitting apart by spaces. If any given word matches the "not detector"
    # I append "not_" as the prefix to all following words until some kind of punctuation is reached. This corrected
    # list of words, adjusted for "not", is saved as n_corrected
    for line in f:
        split_line = line.split()
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

        # 3) I update the Counter objects with lists of words. The Counter defaults any given value to 0, then
        # increments it by 1 anytime it sees that element in a List. It's good at handling duplicates as well as
        # potential errors. By passing in n_corrected for every line, I am placing every word in the input file (except
        # for filenames and review designators) as either a class 0 word or a class 1 word. The class number is listed
        # in our training file immediately following filenames. Once I have these master lists, I can use them later on
        # to calculate accurate log ratios.
        if n_corrected[1] == str(0):
            word_0_counter.update(n_corrected[2:])

            # 4) I do the same thing with bigram features using the zip_longest and islice functions. This specification
            # takes two tokens at a time from my list, saves them as "[token_1_name] [token_2_name]" in a bigram list,
            # then updates the appropriate Counter with that bigram list. The islice is overlapping (each "step" is only
            # a length of one) which means it gets every sequence of two elements, not just every other.
            the_long_zip = zip_longest(n_corrected, islice(n_corrected[2:], 1, None))
            word_0_counter.update([str(ele[0]) + " " + str(ele[1]) for ele in the_long_zip])
        # 3) & 4) This else statement does the unigram and bigram stuff as described above but for class 1 (positive)
        # words
        elif n_corrected[1] == str(1):
            word_1_counter.update(n_corrected[2:])

            the_long_zip = zip_longest(n_corrected, islice(n_corrected[2:], 1, None))
            word_1_counter.update([str(ele[0]) + " " + str(ele[1]) for ele in the_long_zip])

    # 3) & 4) Counter objects support set addition (union operation) so I create a master list of the TOTAL occurrences
    # of all words in the input file. It works very intuitively by adding any existing counts and assuming a count is 0
    # if it's not listed somewhere
    word_total_counter = word_0_counter + word_1_counter

    # 7) I create dictionaries for both values and strengths of all the given words. These will be useful for formatting
    # and sorting
    value_dictionary = {}
    strength_dictionary = {}

    # 5) I calculate smoothed log ratios for all of the total features that have been recorded from the input file.
    # I use LaPlace smoothing (add 1 to both counts) to prevent divide by zero errors. I take the logarithm (base 2)
    # of the quotient of these modified counts. This has the effect of making larger positive numbers for words that
    # are used more frequently in class 1 and less frequently in class 0. Frequent class 0 words become very negative
    for x, count in word_total_counter.most_common(len(word_total_counter)):
        log_ratio = math.log((word_1_counter[x] + 1) / (word_0_counter[x] + 1), 2)

        # 6) If the log ratio is negative, the decision is that the word is a class 0 dominant word. Otherwise it's a
        # class 1 dominant word. With this information, I have the decision numbers and I can set strengths as absolute
        # values (their magnitude of predictive power).
        if not log_ratio == 0:
            if log_ratio < 0:
                value_dictionary[x] = 0
            else:
                value_dictionary[x] = 1
            strength_dictionary[x] = abs(log_ratio)

    f.close()

    # 8) I open the output file
    f = open(output_name, "w")

    # 7) I set the strength dictionary equal to a sorted version of itself using the sort function. This dictionary
    # holds absolute values of log ratios (magnitudes)
    # 8) I then print the first 100,000 words in order of strengths and print off each of their associated
    # classifications as well
    strength_dictionary = sorted(strength_dictionary.items(), key=lambda k: k[1], reverse=True)
    for x, count in strength_dictionary[:100000]:
        f.write('%20s     %1d     %3f' % (x[:20], value_dictionary[x], count)+"\n")
    f.close()

    # 9) I print a top 10 preview of the decision list just as a sanity check for the user to confirm everything worked
    print("Top 10 Preview\n(0 = negative, 1 = positive)")
    print("---------------------------------------")
    for x, count in strength_dictionary[:10]:
        print('%20s     %1d     %3f' % (x[:20], value_dictionary[x], count))


if __name__ == "__main__":
    main(sys.argv[1:])
