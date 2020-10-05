#!/usr/bin/python

import glob
import os
import random
import re
import sys


def bi_gram_array(word, population):
    return_array = []
    for x in range(len(population) - 1):
        if word != '' and word == population[x]:
            return_array.append(population[x + 1])
        elif word == '' and re.match(r"[.!?]", population[x]):
            if re.match(r"[a-z]+", population[x + 1], re.MULTILINE | re.IGNORECASE):
                return_array.append(population[x + 1])
    return return_array


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
    current_string = ""
    n = int(argv[0])
    m = int(argv[1])
    file_names = []

    print("\nRandom Talker made by Jacob Schnoor. CS 4242.\n")
    print("Using a " + str(n) + "-gram model to generate " + str(m) + " random sentences\nFiles:\n")

    if argv[2] == '-f':
        os.chdir(argv[3])
        for file in glob.glob("*.txt"):
            file_names.append(file)
    else:
        for x in argv[2:]:
            file_names.append(x)
    for x in file_names:
        print(x)

    language_model = []
    for x in file_names:
        f = open(x, encoding='utf8')
        for y in f.read().lower():
            if re.match(r"[.!?,;:\']+", y, re.MULTILINE | re.IGNORECASE):
                if current_string != '':
                    language_model.append(current_string)
                language_model.append(y)
                current_string = ""
            elif re.match(r"[^a-z0-9.!?,\']+", y, re.MULTILINE | re.IGNORECASE):
                if current_string != '':
                    language_model.append(current_string)
                current_string = ''
            else:
                current_string = current_string + y
    print("\nTotal Tokens: " + str(len(language_model)))
    print("\nSentences:\n")

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


if __name__ == "__main__":
    main(sys.argv[1:])
