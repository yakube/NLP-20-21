import re
from random import *
from profanity_check import predict, predict_prob

name = ''
my_rand_int = randint(0, 19)


# input:        string that contains a user's first name
# output:       the user's first name
# description:  scans the sentence for instances such as "my name is..." or "i am..." then
#               grabs the following word. otherwise it will just grab the first word
def name_extractor(test_str):
    regex = r"((.*\bmy\sname\sis\s)|(.*\bi\sam\s)|(.*\bi'?m\s)|(^\s))?(\S+)\b(.*)"
    subst = "\\6"
    result = re.sub(regex, subst, test_str, 0, re.MULTILINE | re.IGNORECASE).capitalize()
    return result


def introduction():
    print("This is Eliza the Academic Advisor, made by Jacob Schnoor\n")
    name = name_extractor(input("[eliza] Hi I'm Eliza. Remind me what your name is again?\n\n"))
    print('\nHi ' + name + '. What is your major?')


# regex = r"(?:(?:I|you|he|she|they|we|it)(?:.*)\s(?:know|think|feel|seem)s?(?:\sthat\s)?(?:\slike\s)?)?(.*)\bme\b([^!\.?\n]*)(.*)$"
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
introduction()
