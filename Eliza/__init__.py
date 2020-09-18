import re
from random import randint
from profanity import profanity

name = major = ''
my_rand_int = randint(0, 19)
said_goodbye = False


def ask_name():
    return [
        '\n[eliza] Hi my name is Eliza. What\'s your name?\n\n'
    ]


def ask_major():
    return [
        '\n[eliza] ' + name + ', that\'s right. I think I remember you from orientation. What is your major?\n\n',
        '\n[eliza] Hi ' + name + '. Tell me again what your major was.\n\n',
        '\n[eliza] Oh, ' + name + '. I knew it was something that started with ' + name[
                                                                                   :1] + '. What\'s your major?\n\n',
        '\n[eliza] Yeah, ' + name + '. I thought you looked familiar. What\'s your major?\n\n',
    ]


def ask_feelings():
    return [
        '\n[eliza] So your major is ' + major + '? How are you liking it so far?\n\n',
    ]


def respond_swear():
    return [
        '\n[eliza] Hey! There\'s no need for that kind of language.\n\n',
        '\n[eliza] Please don\'t use profanity.\n\n',
        '\n[eliza] That is highly inappropriate.\n\n',
    ]


def respond_bye():
    return [
        '\n[eliza] Oh, are you leaving?\n\n',
        '\n[eliza] Is that all you needed?\n\n',
        '\n[eliza] Will that be all for today?\n\n',
    ]


def topic_change():
    return [
        '\n[eliza] Anyways, like I was saying...',
    ]


def is_swearing(user_in):
    return profanity.contains_profanity(user_in)


# def is_question(user_in):
#     return True


def is_leaving(user_in):
    # regex = r".*((\bgoodbye\b)|(\bfarewell\b)|(\bstop\b)|(\bexit\b)|(\bi'?m\sleaving\b)|((\bto\b)|(" \
    #         r"\bgonna\b)\sleave\b)).* "
    # return not re.match(regex, user_in, re.MULTILINE | re.IGNORECASE) is None
    return user_in == 'goodbye'


def is_derailment(user_in):
    global said_goodbye
    off_topic = False
    if is_swearing(user_in):
        off_topic = True
    # elif is_question(user_in):
    #     off_topic = True
    elif is_leaving(user_in):
        off_topic = True
        said_goodbye = True
    return off_topic


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


# input:        string containing any number of topics to derail conversation
# output:       the user's answer to the original question
# description:  calls clean_input, question_input, etc. to scan for any immediate things to address
def scan(options):
    if said_goodbye:
        user_in = 'GOODBYE'
    else:
        user_in = input(randologue(options))
        if is_derailment(user_in):
            while is_derailment(user_in):
                response = '\n[eliza] ...\n'
                if is_swearing(user_in):
                    response = randologue(respond_swear())
                # elif is_question(user_in)
                #     response = respond_question(user_in)
                elif is_leaving(user_in):
                    response = randologue(respond_bye())
                user_in = input(response)
            if not said_goodbye:
                print(randologue(topic_change()))
            user_in = scan(options)
    return user_in


# input:        string that contains a user's first name
# output:       the user's first name
# description:  scans the sentence for instances such as "my name is..." or "i am..." then
#               grabs the following word. otherwise it will just grab the first word
def extract_name(test_str):
    regex = r"((.*\bmy\sname\sis\s)|(.*\bi\sam\s)|(.*\bi'?m\s)|(^\s))?(\S+)\b(.*)"
    subst = "\\6"
    result = re.sub(regex, subst, test_str, 0, re.MULTILINE | re.IGNORECASE).title()
    return result


# input:        string that contains a user's major
# output:       the user's major
# description:  scans the sentence for instances such as "my major is..." or "i'm studying..." then
#               grabs the following words. otherwise it will just grab the first words
def extract_major(test_str):
    regex = r"(^.*((\bis\b)|(\bwas\b)|(\bbe\b)|(\bit'?s\b)|(\bstudy(ing)?\b))\s)?(.*)"
    subst = "\\9"
    result = re.sub(regex, subst, test_str, 0, re.MULTILINE | re.IGNORECASE).title()
    return result


def extract_feelings(test_str):
    return test_str


# description:  the main sequence of greetings to begin conversation with Eliza
#               links to various other parts of the program
def main_script():
    global name, major
    print("This is Eliza the Academic Advisor, made by Jacob Schnoor")
    name = extract_name(scan(ask_name()))
    major = extract_major(scan(ask_major()))
    feelings = extract_feelings(scan(ask_feelings()))
    if name == '':
        print('\n[eliza] See ya\n\n')
    else:
        print('\n[eliza] It was nice talking to you, ' + name + '. Have a great rest of your day.')


main_script()

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
