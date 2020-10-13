# --------------------------------------------
# Random Talker
# Made by Jacob Schnoor
# 10/5/20
#
# ==What is it?
#
# The Random Talker is a program that uses unigram, bigram, and trigram language models to scan through real world
# text and generate random sentences. The unigram model is the easiest way to make random sentences. It merely scans
# each word in the text, sees how often they occur, and uses that percentage as the probability that any given word
# will be that word.
#
# For example, the word "the" is usually the most common word in English texts. If it occurs say 2.3% of the time,
# then at each given word, there's a 2.3% chance the random word chosen will be "the".
#
# Bigram and trigram models are more sophisticated and make use of context clues to decide the random word. Bigrams
# look at the last word that was just printed off (let's assume it's "the") and decide from there the likelihoods of
# the following words. Let's say in 90% of cases, the word "the" is followed by "cat". Then, given that a "the" was
# just printed off, there's a 90% chance the next word will be "cat". Trigrams, and more generally n-grams,
# extend this reasoning further and further back to multiword strings. For this program though, trigrams are as high
# as we go, mainly just due to limitations in training data size.
#
# ==How do I use it?
#
# The Random Talker is run through Python on the command line and expects at least one valid .txt file to draw
# training data from
#
# Launching it can take the format of either:
#
# 	python Talker n m file_name.txt second_file_name.txt and_so_on.txt [...]
# or
# 	python Talker n m -f folder_name
#
# Where 	n is the value of n-gram (1=unigram, 2=bigram, 3=trigram)
# 	m is the number of sentences to generate
# 	file_name.txt (and all the other .txt files) are valid .txt files containing text
# 	folder_name is a valid folder containing valid .txt files
#
# Example: python Talker 3 5 -f talker_text
#
# Random Talker made by Jacob Schnoor. CS 4242.
#
# Using a 3-gram model to generate 5 random sentences
# Files:
#
# 1080-0.txt
# 11-0.txt
# 1250-0.txt
# 1342-0.txt
# 1514-0.txt
# 1661-0.txt
# 1952-0.txt
# 205-0.txt
# 25344-0.txt
# 2701-0.txt
# 36-0.txt
# 408-0.txt
# 43-0.txt
# 46-0.txt
# 74-0.txt
# 84-0.txt
# 98-0.txt
# pg1232.txt
# pg1260.txt
# pg1497.txt
# pg16328.txt
# pg16643.txt
# pg23.txt
# pg2542.txt
# pg5200.txt
#
# Total Tokens: 2366967
#
# Sentences:
#
# Clay , the cloth was spread .
#
# What about ?
#
# It came casually , in this whirl and the life and after sitting a little .
#
# Now as i terminated my musings , and i repeat this to alarm lucie into saying , had i judged it best to th
# em , an hour , tearfully thanking gregor ' s chamber .
#
# There she blows — she is unable to arrange , — pearl would frown , “ is he not having allowed himself time
#  to rectify mistakes which may be false , like one of the atlantic a shattered wreck — the polygamous clan
#  life under the shelter of your reasoning is certainly not within another minute or so i am convinced that
#  you should listen to the voice was tremulously sweet , generous heart ; in every morning ’ s adventures i
# n wonderland , though to the haunted house , rousing the population belong to their shivering frames , and
#  i must not expect it : no doubt lots who had no mercy , ” reasserted itself .
#
# *In this example, talker_text was a folder containing all the files that got listed out
# *Sentences vary quite a bit in length
#
# ==How does it work?
#
# The program mainly works by cleaning up text, chopping it into words and punctuation, and pumping out random
# elements from an array.
#
# To start off, all the texts that I have used in my examples come from Project Gutenberg (
# https://www.gutenberg.org/), but any valid .txt file will work with this program. After initially processing user
# commands, the first thing Random Talker does is read through every .txt file. It does a subsititution where every
# non-alphanumeric character gets surrounded on both sides by a space. This has the advantage of separating
# punctuation from their immediate word neighbors.
#
# Next it splits the file using the .split() command. By specifying any number of whitespace characters in the split,
# Random Talker cleanly adds every word and every punctuation mark as a separate element in an overall array called
# language_model.
#
# After language_model is fully created, Random Talker makes heavy use of Python's random library to randomly pick
# out an element from an array. For unigram models this is easy, literally just pick any random element from
# language_model and keep going until you hit a period, exclamation point, or question mark.
#
# For bigrams and trigrams, there's a little bit more of a filtering process. Instead of randomly picking any word
# from any of the files, Random Talker creates temporary arrays of eligible follow-up words. So if "the" was the
# previous word, there will be a relatively small array containing only the elements that have, at some point,
# immediately followed "the". For trigrams, it would be all eligible words that have immediately followed the
# previous two words.
#
# Fortunately, using arrays with Python's random library is incredibly easy and, since duplicates are not filtered
# out, they preserve the proper probabilities of any given word.
# --------------------------------------------

import glob
import os
import random
import re
import sys


# input:        the prior word and the population of words to pick from
# output:       an array of eligible follow-up words
# description:  this method takes in any given word, as well as the pool of words from language_model, and spits out an
#               array of all eligible words to be chosen from. these are the words that immediately come after the
#               specified word. edge cases involving start of sentence are handled with if statements
def bi_gram_array(word, population):
    return_array = []
    for x in range(len(population) - 1):
        if word != '' and word == population[x]:
            return_array.append(population[x + 1])
        elif word == '' and re.match(r"[.!?]", population[x]):
            if re.match(r"[a-z]+", population[x + 1], re.MULTILINE | re.IGNORECASE):
                return_array.append(population[x + 1])
    return return_array


# input:        the two prior words and the population of words to pick from
# output:       an array of eligible follow-up words
# description:  this method takes in any two words, as well as the pool of words from language_model, and spits out an
#               array of all eligible words to be chosen from. these are the words that immediately come after the two
#               specified words. edge cases involving start of sentence are handled with if statements
def tri_gram_array(previous_word, word, population):
    return_array = []
    for x in range(len(population) - 2):
        if previous_word == '':
            if word != '' and re.match(r"[.!?]", population[x]) and word == population[x + 1]:
                return_array.append(population[x + 2])
            elif word == '' and re.match(r"[.!?]", population[x + 1]):
                if re.match(r"[a-z]+", population[x + 2], re.MULTILINE | re.IGNORECASE):
                    return_array.append(population[x + 2])
        else:
            if previous_word == population[x] and word == population[x + 1]:
                return_array.append(population[x + 2])

    return return_array


# input:        the two prior words, the population of words to pick from, and the value of n
# output:       a randomly selected follow-up word
# description:  this method randomly picks an element from language_model, bi_gram_array(), or tri_gram_array()
#               depending on if the user specified unigram, bigram, or trigram modeling
def pick_random_element(previous_word, word, population, n):
    if n <= 1:
        return random.choice(population)
    elif n == 2:
        return random.choice(bi_gram_array(word, population))
    elif n == 3:
        return random.choice(tri_gram_array(previous_word, word, population))
    else:
        return None


def main(argv):
    # The first two arguments specify n-gram degree and number of sentences respectively
    n = int(argv[0])
    m = int(argv[1])

    # Declaration
    file_names = []
    language_model = []

    # Welcome text
    print("\nRandom Talker made by Jacob Schnoor. CS 4242.\n")
    print("Using a " + str(n) + "-gram model to generate " + str(m) + " random sentences\nFiles:\n")

    # Looks for either -f followed by a folder or a sequence of .txt files
    if argv[2] == '-f':
        os.chdir(argv[3])
        for file in glob.glob("*.txt"):
            file_names.append(file)
    else:
        for x in argv[2:]:
            file_names.append(x)

    # Every .txt file is spaced apart, chopped up, and has all words and punctuation thrown into language_model
    for x in file_names:
        f = open(x, encoding='utf8')
        f_string = re.sub(r"([^a-z0-9\s])", " \\1 ", f.read().lower())
        for y in re.split(r"\s+", f_string):
            language_model.append(y)
        print(x)
        f.close()

    # Informational text
    print("\nTotal Tokens: " + str(len(language_model)))
    print("\nSentences:\n")

    # For m number of sentences, choose a start-of-sentence word, then the next word, then the next word...
    # Keeping track of the previous two words at all times just in case
    # Add word after word to the output string then finally print it off when you hit . ! or ?
    for x in range(m):
        output_string = ''
        previous_element = ''
        random_element = pick_random_element('', '', language_model, n)
        while not re.match(r'[.!?]', random_element):
            output_string = output_string + random_element + ' '
            baton_passer = random_element
            random_element = pick_random_element(previous_element, random_element, language_model, n)
            previous_element = baton_passer
        if re.match(r'[.!?]', random_element):
            print(output_string.capitalize() + random_element + "\n")


# Handles passing in the command line arguments
if __name__ == "__main__":
    main(sys.argv[1:])
