# --------------------------------
# Similar PMI
# Made by Jacob Schnoor
# 11/3/20
#
# ==What is it?
#
# The Similar PMI program is a language analysis tool that can take in a large corpus of words being used in a
# variety of sentences and tell the user something about some of those words. By specifying a list of word pairs,
# the user can receive information about the occurrences, both separate and joint, of the words as well as PMI and
# Cosine values (measures of similarity). This is useful as an empirical approach to the question of synonimity.
# Often times when we seek to find synonyms for a word, we look for other words that can be used in nearly identical
# settings. For example, the words "car" and "automobile" are almost interchangeable so we should expect a high
# cosine value of close to 1. This program then follows the general philosophy of Wittgenstein, "The meaning of a
# word is its use in the language."
#
# ==How do I use it?
#
# The similar PMI program runs in Python off the commandline with the following format
#
# 	python Similar_PMI window_size corpus_folder_name test_pairs_name
#
# Where window_size is an integer that sets the "window" for assessing word colocation. If word 1 occurs within [
# window_size] (plus or minus) of word 2, then they co-occur. Common sizes include anywhere from 2 - 5.
#
# corpus_folder_name specifies the name of the folder that contains appropriately formatted .txt files with corpus
# text in them. test_pairs_name specifies the filename of an appropriately formatted .txt file with word pairs to
# look at. The resulting output will list all these word pairs along with their respective statistics. An example is
# as follows:
#
# 	python Similar_PMI 3 PA4-News-2011 word-pairs.txt
#
# Similar to a Point. CS4242. Made by Jacob Schnoor
# Computing similarity from a word by word PMI co-occurrence matrix
#
# Window Size:            3
# Corpus Folder:          PA4-News-2011
# Test Pairs File:        word-pairs.txt
#
# Tokens =                45783633
# Types =                 198211
#
# Cosine          Word 1          Word 2          Word 1 Count    Word 2 Count    Co-Count        PMI
# ------          ------          ------          ------------    ------------    --------        ---
# 0.72492         line            cord            10525           176             0               -999.99999
# 0.82979         line            queue           10525           99              2               6.45744
# 0.67486         line            text            10525           2112            0               -999.99999
# 0.67897         car             automobile      12353           394             4               5.23370
# 0.44752         swedish         finnish         856             220             0               -999.99999
# 0.67665         scientific      interest        1528            8239            16              5.86265
# 0.26759         abdullah        shah            315             298             4               10.92995
# 0.76722         baseball        football        1554            6619            16              6.15416
# 0.85452         baseball        soccer          1554            1212            10              7.92531
# 0.43764         clinton         bush            5423            3839            22              5.59637
# 0.31517         clinton         gore            5423            310             8               7.76733
# 1.00000         clinton         clinton         5423            5423            4               2.63858
# 0.85759         russia          germany         3382            3983            36              6.93495
# 0.61359         russia          mexico          3382            4106            21              6.11347
# 0.61359         mexico          russia          4106            3382            21              6.11347
# 0.04751         duluth          minnesota       174             1673            0               -999.99999
# 0.00966         duluth          fargo           174             470             0               -999.99999
# 0.10460         duluth          paris           174             2974            0               -999.99999
# 0.57612         woman           homemaker       10674           63              3               7.67420
# 0.59906         man             homemaker       22142           63              3               6.62151
# 0.55536         woman           surgeon         10674           643             0               -999.99999
# 0.60796         man             surgeon         22142           643             0               -999.99999
# 0.70722         boy             brave           3053            474             0               -999.99999
# 0.66262         girl            brave           5393            474             0               -999.99999
# 0.78136         king            queen           4968            1186            23              7.48155
# 0.62459         king            man             4968            22142           0               -999.99999
# 0.59267         king            woman           4968            10674           0               -999.99999
# 0.61416         queen           man             1186            22142           0               -999.99999
# 0.56230         queen           woman           1186            10674           0               -999.99999
# -999.99999      babbage         lovelace        0               8               0               -999.99999
# 0.17152         ted             roosevelt       3180            218             0               -999.99999
# 0.04206         ted             pedersen        3180            36              0               -999.99999
# 0.23034         ted             johnson         3180            4466            0               -999.99999
# 0.23160         turtle          tortoise        153             12              0               -999.99999
# 0.53209         turtle          bird            153             1712            0               -999.99999
# 0.41364         turtle          shoe            153             515             0               -999.99999
# 0.51848         pizza           spaghetti       860             80              0               -999.99999
# 0.14857         pizza           calzone         860             4               0               -999.99999
# 0.92951         man             person          22142           8663            0               -999.99999
# 0.88655         woman           person          10674           8663            4               0.98586
#
# ==How does it work?
#
# The Similar PMI program makes use of the Counter object which is a high performance container type in Python,
# as well as the zip method which I go into more detail about later on. In essence the program has the following
# procedure.
#
# 	1. Split command arguments
# 	2. Introduce user
# 	3. Scan all word pairs as tuples into a Counter
# 	4. Calculate co-count
# 	5. Calculate PMI
# 	6. Calculate Cosine
# 	7. Gather other statistics
# 	8. Print these results to the user
#
# I go into more detail in the code
import glob
import os
import re
import sys
from collections import Counter
from itertools import islice
from math import sqrt, log

# 3. The word_pairs and word_counter objects are both vital to this program. The Counter is a high performance container
# type that can quickly handle duplicates and assign accurate counts to each respective element. Elements that are never
# added have a default value of 0 (rather than throwing an error)

# word_pairs records tuples of every pair of two words that is found in the corpus within a window size. Unfortunately,
# order matters so these pairs must be "translated" in the get_coconut() function. The tuples are relatively easy to
# create using a for loop and the "zip" function later on. While not technically a matrix, the word_pairs Counter holds
# onto raw counts and is relatively easy to iterate through in the code. Using these raw counts, all vital statistics
# can be calculated as needed

# word_counter is simpler. It just gets updated with every token. Duplicate tokens are assimilated intuitively by
# incrementing the relevant element. The length of word_counter is the number of unique tokens. The sum of all its
# counts represents the total number of tokens in the corpus
word_pairs = Counter([])
word_counter = Counter([])


# 4. The co-count of any word pair is calculated by accessing the relevant tuples in the word_pairs Counter object
# In tuples, order matters. This method grabs both possible permutations of any two requested words and returns their
# sum. In essence, it translates from "ordered pairs" into "collocated words"
def get_coconut(word_1, word_2):
    return word_pairs[tuple((word_1, word_2))] + word_pairs[tuple((word_2, word_1))]


# 5. The PMI calculates the observed probability of word_1 and word_2 co-occurring versus what would be expected if
# their probabilities were independent. It calculates the independent probabilities of word_1 and word_2 by dividing
# their counts by the total number of tokens in the corpus. It also accesses the co-count of word_1 and word_2 and finds
# the probability of that. Then it returns the log base 2 of the joint probability divided by the product of the
# independent probabilities.
# log2( P(x,y) / ( P(x)*P(y) ) )
def get_pmi(word_1, word_2):
    total = sum(word_counter.values())
    prob_1 = word_counter[word_1] / total
    prob_2 = word_counter[word_2] / total
    prob_coconut = get_coconut(word_1, word_2) / total
    if prob_1 == 0 or prob_2 == 0 or prob_coconut == 0:
        return -999.99999
    else:
        return log(prob_coconut / (prob_1 * prob_2), 2)


# 6. The cosine calculates the similarity of two words on a scale of -1 to 1. It does this by finding the dot product
# of word_1 and word_2's vectors, v and w respectively. Then it divides this dot product by the product of lengths of
# the associated vectors.
# For every unique word in the corpus, the get_cosine method adds on a v-w product to v_w_sum, a v^2 to the
# v_squared_sum, and a w^2 to the w_squared sum. These mathematical sums represent the dot product, and the two vector
# lengths squared.
# Assuming the denominator isn't a zero, get_cosine returns the dot_product divided by the product of vector lengths
# Cosine(v,w) =    v·w
#                 |v||w|
# Note: To avoid divide-by-zero errors, -999.99999 is sometimes given as a dummy value
def get_cosine(word_1, word_2):
    v_w_sum = 0
    v_squared_sum = 0
    w_squared_sum = 0
    for element in list(word_counter):
        v = get_coconut(word_1, element)
        w = get_coconut(word_2, element)
        v_w_sum = v_w_sum + (v * w)
        v_squared_sum = v_squared_sum + (v * v)
        w_squared_sum = w_squared_sum + (w * w)
    denominator = sqrt(v_squared_sum) * sqrt(w_squared_sum)
    if denominator == 0:
        return -999.99999
    else:
        return v_w_sum / denominator


def main(argv):
    # 1. The program splits command arguments and assigns them to variables
    window_size = int(argv[0])
    corpus_folder_name = argv[1]
    test_pairs_name = argv[2]

    test_pairs = open(test_pairs_name, encoding='utf8')

    # 2. Introduces the user with background information
    print("\nSimilar to a Point. CS4242. Made by Jacob Schnoor")
    print("Computing similarity from a word by word PMI co-occurrence matrix\n")
    print("Window Size:    \t" + str(window_size))
    print("Corpus Folder:  \t" + corpus_folder_name)
    print("Test Pairs File:\t" + test_pairs_name + "\n")

    # 3. This section scans all respective counts into the relevant Counter objects
    # For every line of every .txt file in the specified corpus folder, chop it up into individual words
    # Update the word_counter Counter object so it has the relevant individual counts of every unique word
    os.chdir(corpus_folder_name)
    for file_name in glob.glob("*.txt"):
        file = open(file_name, encoding='utf8')
        for line in file:
            words = re.sub(r"[^[a-z0-9\s]", "", line, 0, re.IGNORECASE).lower().split()
            word_counter.update(words)

            # 3. For every integer from 1 to the window size, update the word_pair Counter object with the tuples of
            # words separated x spaces apart.
            # This essentially takes a line of text along with a given window_size, and explicitly lists out all valid
            # ordered pairs of word co-occurrences. It uses this list of all recorded tuples to update the word_pairs
            # Counter object

            # For example, take the sentence "mary had a little lamb"
            # When x = 1
            #   (mary, had)
            #   (had, a)
            #   (a, little)
            #   (little, lamb)
            # When x = 2
            #   (mary, a)
            #   (had, little)
            #   (a, lamb)
            # When x = 3
            #   (mary, little)
            #   (had, lamb)
            # When x = 4
            #   (mary, lamb)
            # ...You get the idea

            # All these ordered pairs are added to the word_pairs Counter, duplicates are dealt with intuitively, and
            # we can access these word co-occurrence counts by merely specifying our two elements to the Counter.
            for x in range(1, window_size):
                word_pairs.update(zip(words, islice(words, x, None)))

    # 7. The program spits out other statistics regarding tokens and unique types. Counter objects are good about
    # handling duplicates so both statistics are easy to grab from the word master list
    print("Tokens =\t\t" + str(sum(word_counter.values())))
    print("Types = \t\t" + str(len(word_counter)) + "\n")

    # 8. This is just some formatting for the printed output
    header = '{0:15s} {1:15s} {2:15s} {3:15s} {4:15s} {5:15s} {6:15s}'
    template = '{0:<15.5f} {1:15s} {2:15s} {3:<15d} {4:<15d} {5:<15d} {6:<15.5f}'

    print(header.format("Cosine", "Word 1", "Word 2", "Word 1 Count", "Word 2 Count", "Co-Count", "PMI"))
    print(header.format("------", "------", "------", "------------", "------------", "--------", "---"))

    # 8. This prints out, row by row, all the statistics of the word pairs from the word pairs file. Cosine, PMI,
    # co-count, and others are trivial to access now that we have functions for them
    for line in test_pairs:
        split_line = line.split()
        word_1 = split_line[0]
        word_2 = split_line[1]

        print(template.format(get_cosine(word_1, word_2), word_1, word_2, word_counter[word_1],
                              word_counter[word_2], get_coconut(word_1, word_2), get_pmi(word_1, word_2)))


if __name__ == "__main__":
    main(sys.argv[1:])
