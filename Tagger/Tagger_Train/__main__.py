# --------------------------------
# Tagger Trainer
# Made by Jacob Schnoor
# 11/17/20
#
# ==What is it?
#
# The Tagger Trainer is the first of a three part program that seeks to do part-of-speech tagging on strings of text.
# This means that ideally, the Tagger programs will be able to look at a previously unseen sentence, and identify
# which words are nouns, which are verbs, which are adjectives, etc. This is useful for a wide variety of
# applications such as identifying named entities.
#
# The Trainer specifically serves the role of scanning a corpus of labeled text. By looking at over a million tokens
# in context, with their correct tags, a probability list can be generated that will be used later on.
#
# ==How do I use it?
#
# The Tagger Trainer is a Python program that runs off the commandline with the following format:
#
# 	python Tagger_Train training_data.txt probability_list.txt
#
# Where training_data.txt is an appropriately formatted .txt file with every line being a word and its respective
# tag. probability_list.txt will be the output file with a list of all unique tokens, their tags, and the likelihood
# of that tag. The list is sorted by likelihood.
#
# As an example. One might type:
#
# 	python Tagger_Train pos-train.txt tagger-train-prob.txt
#
# And get the following output in tagger-train-prob.txt
#
# ,                             	,    	0.999305
# .                             	.    	0.999128
# the                           	DT   	0.998869
# of                            	IN   	0.998383
# to                            	TO   	0.998367
# and                           	CC   	0.997449
# a                             	DT   	0.997096
# $                             	$    	0.995225
# ``                            	``   	0.995216
# ''                            	''   	0.995209
# 		.
# 		.
# 		.
# a                             	IN   	0.000081
# to                            	JJ   	0.000069
# the                           	CD   	0.000037
# the                           	NN   	0.000037
# the                           	VBP  	0.000037
#
# (The list has about 59,000 lines)
#
# ==How does it work?
#
# The Tagger Trainer is broken down into a few main parts (more details can be found in the code):
#
# 	1) Initialize variables, open files, and introduce user
# 	2) Split entire input file into array based on slashes and newline characters
# 	3) Update word_counter, tag_counter, and word_tag_pairs with all the words and their respective tags
# 	4) Create sorted dictionary of word-tag pair likelihoods
# 	5) Write this list in a readable way to the output file
# 	6) Indicate completion

import re
import sys
from collections import Counter
from itertools import islice

# 1) This establishes the Counter objects and the dictionary object. Counters are high performance containers and are
# very useful for counting up large amounts of unique token types. The dictionary makes for easy sorting later on
word_tag_pairs = Counter([])
word_counter = Counter([])
tag_counter = Counter([])
word_tag_probs = dict()


def main(argv):
    # 1) Splits user arguments into the input filename and the output filename
    input_filename = argv[0]
    output_filename = argv[1]

    # 1) Introduces the user and gives brief information
    print("\nPOS Tagger Trainer. CS4242. Made by Jacob Schnoor\n")
    print("Training data:    \t" + input_filename)
    print("Probability file: \t" + output_filename + "\n")

    # 2) Reads the whole input file at once and breaks it apart using re.split(). This results in about half the list
    # being blank or newline characters. But luckily, since the file is well formatted, every four elements are of the
    # same type.
    # e.g. list might be = ["","The","DT","\n","","seven","CD","\n",...etc.]
    r_split = re.split(r"(.*)(?<!\\)\/(.*)", open(input_filename, encoding="utf8").read())

    # 3) This section updates all the relevant counters based on the list we just obtained. By using islice(),
    # we essentially say, "Start at element x, end at element y, and increment by z". Since our list has a certain
    # regularity to it, it becomes trivial to grab all words, all tags, and all word-tag pairs. The Counter objects
    # can efficiently count them up and deal with duplicates. We will deal with these raw counts to determine our
    # probabilities.
    word_counter.update(islice(r_split, 1, None, 3))
    tag_counter.update(islice(r_split, 2, None, 3))
    word_tag_pairs.update(zip(islice(r_split, 1, None, 3),
                              islice(r_split, 2, None, 3)))

    # 4) We open the output file for writing. Then we make our dictionary of probabilities based on raw counts and
    # LaPlace smoothing. For every word-tag pair that we find in our Counter object, we calculate probability by
    # taking the occurrences of the word and tag together plus one, then divide by how many times that word occurs plus
    # how many total tags there are.

    # The reason we use LaPlace smoothing is that probability ordering is normally skewed toward rare events. For
    # example, if a word only occurs once, then that word-tag pair would have a 100% chance of being the case, whereas
    # something with 499/500 occurrences would be ranked lower on the list. I figured that a LaPlace smoothed list
    # would be in a more useful order.
    out = open(output_filename, "w")
    for word, tag in word_tag_pairs:
        word_tag_probs[(word, tag)] = (word_tag_pairs[(word, tag)] + 1) / (word_counter[word] + len(tag_counter))

    # 5) We sort the list first based on probability, then alphabetically if the probabilities are equal.
    # For every element in this list, we print out the word, the tag, and the probability. This gets written to the
    # output file.
    for x in sorted(word_tag_probs, key=lambda y: (-word_tag_probs[y], y)):
        out.write("{:30s}\t{:5s}\t{:8f}\n".format(x[0], x[1], word_tag_probs[x]))
    out.close()
    # 6) "DONE" is printed off to indicate that the process is complete.
    print("DONE")


if __name__ == "__main__":
    main(sys.argv[1:])
