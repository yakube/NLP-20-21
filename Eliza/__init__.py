import re
from random import randint
from profanity import profanity

global name, major
my_rand_int = randint(0, 19)


# input:        array of dialogue options to be cycled through
# output:       the dialogue string that is chosen
# description:  selects an element in an array of up to 20 discrete dialogue options
#               by cycling through sequentially then wrapping around (using modulo division)
#               the starting point is randomized at startup in the variable, my_rand_int
def randologue(option_array):
    global my_rand_int
    option = option_array[my_rand_int % len(option_array)]
    my_rand_int = my_rand_int + 1
    if my_rand_int > 19:
        my_rand_int = 20
    return option


# input:        string that may potentially contain offensive or abusive language
# output:       a string containing no profanity
# description:  uses the profanity module to detect foul language. requests the user
#               to rephrase themselves until no profanity is present
def clean_input(eliza_string):
    user_in = input(eliza_string)
    while profanity.contains_profanity(user_in):
        options = [
            "\n[eliza] Hey! There's no need for that kind of language.\n",
            "\n[eliza] Please don't use profanity.\n",
            "\n[eliza] That is highly inappropriate.\n"
        ]
        print(randologue(options))
        print("[eliza] Now like I was saying...")
        user_in = input(eliza_string)
    return user_in


# input:        string that contains a user's first name
# output:       the user's first name
# description:  scans the sentence for instances such as "my name is..." or "i am..." then
#               grabs the following word. otherwise it will just grab the first word
def name_extractor(test_str):
    regex = r"((.*\bmy\sname\sis\s)|(.*\bi\sam\s)|(.*\bi'?m\s)|(^\s))?(\S+)\b(.*)"
    subst = "\\6"
    result = re.sub(regex, subst, test_str, 0, re.MULTILINE | re.IGNORECASE).title()
    return result


# input:        string that contains a user's major
# output:       the user's major
# description:  scans the sentence for instances such as "my major is..." or "i'm studying..." then
#               grabs the following words. otherwise it will just grab the first words
def major_extractor(test_str):
    regex = r"(^.*((\bis\b)|(\bwas\b)|(\bbe\b)|(\bit'?s\b)|(\bstudy(ing)?\b))\s)?(.*)"
    subst = "\\9"
    result = re.sub(regex, subst, test_str, 0, re.MULTILINE | re.IGNORECASE).title()
    return result


# input:        none. the major is stored globally
# output:       a string containing trivial banter about the user's major
# description:  generates a string of the form "{person i know} is a ____ major as well"
def congratulate_major():
    person = [
        "My mom",
        "My dad",
        "My cousin",
        "My friend",
        "My neighbor",
        "My pen pal",
    ]
    result = "\n[eliza] Oh wow! " + randologue(
        person) + " is a " + major + " major actually. How are you liking it so far?\n\n"
    return result


# description:  the main sequence of greetings to begin conversation with Eliza
#               links to various other parts of the program
def introduction():
    global name, major
    print("This is Eliza the Academic Advisor, made by Jacob Schnoor")
    user_in = clean_input("\n[eliza] Hi I'm Eliza. Remind me what your name is again?\n\n")
    name = name_extractor(user_in)
    user_in = clean_input('\n[eliza] ' + name + ', that\'s right. I think I remember you from orientation. What is '
                                                'your major?\n\n')
    major = major_extractor(user_in)
    user_in = clean_input(congratulate_major())
    # sentiment analysis

introduction()

# regex = r"(?:(?:I|you|he|she|they|we|it)(?:.*)\s(?:know|think|feel|seem)s?(?:\sthat\s)?(?:\slike\s)?)?(.*)\bme\b([
# ^!\.?\n]*)(.*)$"
#
# test_str = input('Why did you come here today?\n'.upper())
#
# subst = "Why do you feel like \\1you\\2?"
#
# result = re.sub(regex, subst, test_str, 0, re.MULTILINE | re.IGNORECASE)
#
# if result:
#     print(result.upper())

# Main
