import re
from random import randint
from profanity import profanity

name = major = ''
my_rand_int = randint(0, 19)
said_goodbye = False


def pronoun_flip(user_in):
    # start out lowercase
    user_in = user_in.lower()

    # expand out contractions
    user_in = re.sub(r"\bi'?m\b", "I am", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(?<=\w)'re\b", " are", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"\bcan'?t\b", "can not", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(?<=\w)n't\b", " not", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(?<=\w)'ll\b", " will", user_in, 0, re.MULTILINE | re.IGNORECASE)

    # convert second person to coded words
    user_in = re.sub(r"(\b(?<=\byou\b\s)\bare\b)", "##a3##", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(\bare\b(?=\s\byou\b))", "##a3##", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(\b(?<=\byou\b\s)\bwere\b)", "##w3s##", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(\bwere\b(?=\s\byou\b))", "##w3s##", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(\byourself\b)", "##m1self##", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(\byours\b)", "##m1ne##", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(\byour\b)", "##m1##", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(^(.*((\bthat\b)|(\bthink\b)|(\bhope\b)|(\bguess\b))\s)?you\b)", "##1##", user_in, 0,
                     re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(\byou\b)", "##m3##", user_in, 0, re.MULTILINE | re.IGNORECASE)

    # convert first person to second person
    user_in = re.sub(r"(\bmyself\b)", "yourself", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(\bmine\b)", "yours", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(\bmy\b)", "your", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(\bme\b)", "you", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(\bi\b)", "you", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(\bam\b)", "are", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(\b(?<=\bi\b\s)\bwas\b)", "were", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(\bwas\b(?=\s\bi\b))", "were", user_in, 0, re.MULTILINE | re.IGNORECASE)

    # convert coded words to first person
    user_in = re.sub(r"(##m1self##)", "myself", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(##m1ne##)", "mine", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(##m1##)", "my", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(##1##)", "I", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(##m3##)", "me", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(##a3##)", "am", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(##w3s##)", "was", user_in, 0, re.MULTILINE | re.IGNORECASE)

    # fixing miscellaneous subject/object confusions
    user_in = re.sub(r"(?<=\bam\b\s)\bme\b", "I", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"\bme\b(?=\s\bam\b)", "I", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(?<=\bwas\b\s)\bme\b", "I", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"\bme\b(?=\s\bwas\b)", "I", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"(?<=\bdo\b\s)\bme\b", "I", user_in, 0, re.MULTILINE | re.IGNORECASE)
    user_in = re.sub(r"\bme\b(?=\s\bdo\b)", "I", user_in, 0, re.MULTILINE | re.IGNORECASE)
    return user_in


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


def ask_hometown():
    return [
        '\n[eliza] What is your hometown?\n\n',
        '\n[eliza] Where are you from?\n\n',
    ]


def ask_gradyear():
    return [
        '\n[eliza] What year do you expect to graduate?\n\n',
        '\n[eliza] When do you think you\'ll graduate?\n\n',
    ]


def ask_other():
    return [
        '\n[eliza] Well if you didn\'t have any other questions then I guess I\'ll be on my way...\n\n',
        '\n[eliza] So I\'m assuming you don\'t have any other questions for me...\n\n',
    ]


def respond_swear():
    return [
        '\n[eliza] Hey! There\'s no need for that kind of language.\n\n',
        '\n[eliza] Please don\'t use profanity.\n\n',
        '\n[eliza] That is highly inappropriate.\n\n',
    ]


def respond_gibberish():
    return [
        '\n[eliza] I\'m sorry. I can\'t understand you.\n\n',
        '\n[eliza] Could you speak a little more clearly?\n\n',
        '\n[eliza] I\'m having difficulty interpreting what you\'re saying.\n\n',
    ]


def respond_question_request():
    return [
        '\n[eliza] Sure. What did you want to ask me?\n\n',
        '\n[eliza] What\'s your question\n\n',
    ]


def respond_question(user_in):
    responses = []

    # Generic response regardless of question type
    regex_total = r"^(.*[\.!,]\s)?((\bcan('?t)?\b)|(\bwould(n'?t)?\b)|(\bis(n'?t)?\b)|(\bare(n'?t)?\b)|(\bwill\b)|(" \
                  r"\bwon'?t\b)|(\bwho('?se?)?\b)|(\bwhat('?s)?\b)|(\bwhere('?s)?\b)|(\bwhen('?s)?\b)|(\bwhy\b)|(\bhow\b)|(" \
                  r"\bshould(n'?t)?\b)|(\bdo(n'?t)?\b))\s([^?\n]*)(\?)?$"

    # Why/where/when do/does/did questions
    regex_why_does = r"^(.*[\.!,]\s)?(\b(why|where|when|how)\s(do(es)?|did)\b)\s([^?\n]*)(\?)?$"

    # How much/many questions
    regex_how_many = r"^(.*[\.!,]\s)?(\bhow\s(many|much)\b)\s([^?\n]*)(\?)?$"

    if re.match(regex_why_does, user_in, re.MULTILINE | re.IGNORECASE):
        subst = "\\3 do you think \\6?"
        statement = re.sub(regex_why_does, subst, pronoun_flip(user_in), 0, re.MULTILINE | re.IGNORECASE)
        responses.append('\n[eliza] ' + statement + '\n\n')
    elif re.match(regex_how_many, user_in, re.MULTILINE | re.IGNORECASE):
        responses.append('\n[eliza] At least ' + str(my_rand_int * 7 + 3) + '\n\n')
    else:
        subst = "Why do you ask \\2 \\27?"
        responses.append(
            '\n[eliza] ' + re.sub(regex_total, subst, pronoun_flip(user_in), 0, re.MULTILINE | re.IGNORECASE) + '\n\n')

    return responses


def respond_bye():
    return [
        '\n[eliza] Oh, are you leaving?\n\n',
        '\n[eliza] Is that all you needed?\n\n',
        '\n[eliza] Will that be all for today?\n\n',
    ]


def respond_apology():
    return [
        '\n[eliza] It\'s okay\n\n',
        '\n[eliza] Apology accepted\n\n',
        '\n[eliza] You are forgiven\n\n',
    ]


def respond_unsure():
    return [
        '\n[eliza] You sound confused.\n\n',
        '\n[eliza] What don\'t you know?\n\n',
        '\n[eliza] Is there something I can clarify for you?\n\n',
    ]


def respond_declaration(user_in):
    responses = []

    user_in = pronoun_flip(user_in)

    # I am ____ statements
    regex_i_am = r"^(.*[\.!?,]\s)?(\bi)(('?m\s)|(\sam\s))(.*)"

    # I ____ statements
    regex_i = r"^(.*[\.!?,]\s)?\bi\b\s(.*)"

    # You are ____ statements
    regex_you_are = r"^(.*[\.!?,]\s)?(\byou)(('?re\s)|(\sare\s))(.*)"

    # You ____ statements
    regex_you = r"^(.*[\.!?,]\s)?\byou\b\s(.*)"

    if re.match(regex_i_am, user_in, re.MULTILINE | re.IGNORECASE):
        subst = "Why am I \\6?"
        statement = re.sub(regex_i_am, subst, user_in, 0, re.MULTILINE | re.IGNORECASE)
        responses.append('\n[eliza] ' + statement + '\n\n')
    elif re.match(regex_i, user_in, re.MULTILINE | re.IGNORECASE):
        subst = "Why do I \\2?"
        statement = re.sub(regex_i, subst, user_in, 0, re.MULTILINE | re.IGNORECASE)
        responses.append('\n[eliza] ' + statement + '\n\n')
    elif re.match(regex_you_are, user_in, re.MULTILINE | re.IGNORECASE):
        subst = "Why are you \\6?"
        statement = re.sub(regex_you_are, subst, user_in, 0, re.MULTILINE | re.IGNORECASE)
        responses.append('\n[eliza] ' + statement + '\n\n')
    elif re.match(regex_you, user_in, re.MULTILINE | re.IGNORECASE):
        subst = "Why do you \\2?"
        statement = re.sub(regex_you, subst, user_in, 0, re.MULTILINE | re.IGNORECASE)
        responses.append('\n[eliza] ' + statement + '\n\n')
    else:
        responses.append('\n[eliza] ...\n\n')

    return responses


def topic_change():
    return [
        '\n[eliza] Anyways, like I was saying...',
        '\n[eliza] So I don\'t think you actually answered this yet...',
        '\n[eliza] So getting back on topic...',
    ]


def is_swearing(user_in):
    return profanity.contains_profanity(user_in)

#---------Find better regex-----------
def is_gibberish(user_in):
    regex = r"(((.*?)(\b[^aeiouy\s\n]+\s)+(.*))|((.*?)(a{3,}|b{3,}|c{3,}|d{3,}|e{3,}|f{3,}|g{3,}|h{3,}|i{3,}|j{3," \
            r"}|k{3,}|l{3,}|m{3,}|n{3,}|o{3,}|p{3,}|q{3,}|r{3,}|s{3,}|t{3,}|u{3,}|v{3,}|w{3,}|x{3,}|y{3,}|z{3,})(.*)))"
    if re.match(regex, user_in, re.MULTILINE | re.IGNORECASE):
        return True
    else:
        return False


def is_question_request(user_in):
    regex = r".*\b(question|ask)\b.*"
    if re.match(regex, user_in, re.MULTILINE | re.IGNORECASE):
        return True
    else:
        return False


def is_question(user_in):
    regex = r"^(.*[\.!,]\s)?((\bcan('?t)?\b)|(\bwould(n'?t)?\b)|(\bis(n'?t)?\b)|(\bare(n'?t)?\b)|(\bwill\b)|(" \
            r"\bwon'?t\b)|(\bwho('?se?)?\b)|(\bwhat('?s)?\b)|(\bwhere('?s)?\b)|(\bwhen('?s)?\b)|(\bwhy\b)|(\bhow\b)|(" \
            r"\bshould(n'?t)?\b)|(\bdo(n'?t)?\b))\s([^?\n]*)(\?)?$"
    if re.match(regex, user_in, re.MULTILINE | re.IGNORECASE):
        return True
    else:
        return False


def is_leaving(user_in):
    regex = r".*((\bgoodbye\b)|(\bfarewell\b)|(\bstop\b)|(\bexit\b)|(\bi'?m\sleaving\b)|(\b(to|will|gonna)\sleave\b)).*"
    if re.match(regex, user_in, re.MULTILINE | re.IGNORECASE):
        return True
    else:
        return False


def is_apologizing(user_in):
    regex = r".*\b(sorry)\b.*"
    if re.match(regex, user_in, re.MULTILINE | re.IGNORECASE):
        return True
    else:
        return False


def is_declaring(user_in):
    regex = r"^(.*[\.!?,]\s)?((\byou\b)|(\bi'?m?\b))(\s(\bam\b)|(\bare\b)|(\bis\b))?(.*)"
    if re.match(regex, user_in, re.MULTILINE | re.IGNORECASE):
        return True
    else:
        return False


def is_unsure(user_in):
    regex = r".*\b(confused?|i\sdon'?t\sknow)\b.*"
    if re.match(regex, user_in, re.MULTILINE | re.IGNORECASE):
        return True
    else:
        return False


def is_derailment(user_in, allow_i_am):
    global said_goodbye
    off_topic = (
            is_swearing(user_in)
            | is_question(user_in)
            | is_question_request(user_in)
            | is_leaving(user_in)
            | is_apologizing(user_in)
            | (is_declaring(user_in) and not allow_i_am)
            | is_unsure(user_in)
            | is_gibberish(user_in)
    )
    if is_leaving(user_in):
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
def scan(options, allow_i_am):
    global said_goodbye
    if said_goodbye:
        user_in = 'GOODBYE'
    else:
        user_in = input(randologue(options))
        if is_derailment(user_in, allow_i_am):
            while is_derailment(user_in, allow_i_am):
                response = '\n[eliza] ...\n\n'
                if is_swearing(user_in):
                    response = randologue(respond_swear())
                elif is_gibberish(user_in):
                    response = randologue(respond_gibberish())
                elif is_question_request(user_in):
                    response = randologue(respond_question_request())
                elif is_question(user_in):
                    response = randologue(respond_question(user_in))
                elif is_apologizing(user_in):
                    response = randologue(respond_apology())
                elif is_unsure(user_in):
                    response = randologue(respond_unsure())
                elif is_leaving(user_in):
                    response = randologue(respond_bye())
                elif is_declaring(user_in) and not allow_i_am:
                    response = randologue(respond_declaration(user_in))
                user_in = input(response)
            if not said_goodbye:
                print(randologue(topic_change()))
            user_in = scan(options, allow_i_am)
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


# description:  the main sequence of greetings to begin conversation with Eliza
#               links to various other parts of the program
def main_script():
    global name, major
    print("This is Eliza the Academic Advisor, made by Jacob Schnoor")
    # print(pronoun_flip(input("Pronoun Flip: ")))
    name = extract_name(scan(ask_name(), True))
    major = extract_major(scan(ask_major(), False))
    scan(ask_feelings(), True)
    scan(ask_hometown(), False)
    scan(ask_gradyear(), False)
    scan((ask_other()), False)
    if name == 'Goodbye':
        print('\n[eliza] See ya')
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
