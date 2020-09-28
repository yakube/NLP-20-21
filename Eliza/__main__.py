# --------------------------------------------
# Eliza the Academic Advisor
# Made by Jacob Schnoor
# 9/24/20
#
# ==What is it?:
#
# Eliza was a program initially created in the 1960s to simulate the role of a Rogerian psychotherapist. Instead of
# providing any concrete answers to specific questions, Eliza would merely manipulate user input and pry deeper into
# WHY users believe certain things about themselves or the world. The program did this largely by taking some input,
# x, and asking "Why do you believe x?" or "Why do you ask x?"
#
# The program I have created uses a similar concept. It provides no genuine information that the user does not
# already know. Instead, it merely asks more and more WHY you are asking about x or why you feel x way.
#
# An example of a user conversation is as follows:
#
# 	Can I ask you a question?
#
# 	[eliza] What's your question
#
# 	What's your favorite color?
#
# 	[eliza] Why do you ask what's my favorite color?
#
# 	I want to know what it is
#
# 	[eliza] Why do you want to know what it is?
#
# And so on, often until the user expresses frustration, confusion, or befuddlement.
#
# The main approach I have taken in trying to simulate a conversation is to essentially have a preset "script" of
# trivial questions for Eliza to ask the user. These questions involve asking for favorite colors, favorite foods,
# hometowns, and so on until the user presumably grows impatient and derails the conversation.
#
# The program has a general detection system for derailment ("is_derailment()"). This general system uses many
# subsystems involving regular expressions to detect possible sources of derailment (things like asking a question,
# swearing, uncertainty, and apologizing)
#
# By using a preset script, along with derailment detection, the goal is that Eliza will always be actively saying
# something to the user. The user on the other hand is free at any point in the dialogue to change topics or ask to
# leave.
#
# If the user gets distracted momentarily, Eliza will attempt to bring the conversation back to trivial questions.
# She will even remember a few pieces of information and incorporate those into her questions.
#
# An example is as follows:
#
# 	[eliza] Could you speak a little more clearly?
#
# 	About what?
#
# 	[eliza] So getting back on topic...
#
# 	[eliza] Why did you decide to study Chemical Engineering?
#
# 	Because math and science
#
# 	[eliza] Are there a lot of Chemical Engineering majors in Inver Grove Heights?
#
# 	Not a lot from Inver Grove but I've met a few people
#
#   [eliza] So Nick, earlier you described Chemical Engineering by saying you think it suits you pretty well. Does that
#    still hold true?
#
# 	Yes
#
#
# ==How Does it work?
#
# Eliza the Academic Advisor can be thought of as having 3 parts:
# 	-The script
# 	-The extraction
# 	-And the derailment
#
# The script is relatively straightforward in a programming sense because all it requires is that Eliza prints off a
# series of prewritten phrases, questions, and so forth. These include, for example, saying things like "Hi,
# my name is Eliza. What's your name?"
#
# A mild complication arises when the user faces repetition in the way questions are phrased. To alleviate this
# somewhat, there are the ask_QUESTION() and respond_DERAILMENT() functions (pattern of names rather than literal
# names). These are mainly just glorified arrays of possible strings that are passed into the randologue() function.
# By using modulo division, and random number generation, the dialogue options are somewhat randomized.
#
#
# The extraction methods are named in the pattern of extract_INFORMATION(). These methods are heavily dependent on
# regular expressions and, like the name suggests, they extract the relevant bit of information from a string of input.
#
# extract_name() for example takes in a statement like "Hello, my name is John Smith and my favorite color is green"
# and returns just the word "John". By using these methods, Eliza can store quick facts about the user and bring them
# up later in conversation as part of her dialogue options.
#
#
# Finally, the derailment system is what makes the conversation less linear. It is realized primarily through the
# scan() function which references many other is_DISTRACTION() type functions. The generic function, is_derailment(),
# calls all the other functions and gives a general consensus on whether the user is really answering the question or
# not.
#
# By using regular expressions, as well as the Profanity library for Python, Eliza can do some basic pattern
# matching. If the user is asking their own question, swearing at the program, or just generally typing gibberish,
# Eliza will respond in the appropriate ways.
#
#
# When all is said and done, Eliza says goodbye to the user and tells them to enjoy the rest of their day.
# --------------------------------------------


import re
from random import randint
from profanity import profanity

name = major = ''
my_rand_int = randint(0, 19)
said_goodbye = False


# type:         miscellaneous
# input:        a string of user input
# output:       the same user input but with "my" turned into "your", "me" turned into "you", etc.
# description:  uses numerous regular expression substitutions to quickly flip pronouns and deal with some common
#               grammatical errors
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


# type:         ask_QUESTION()
# input:        n/a
# output:       an array of possible "What's your name?" questions to ask
# description:  an array of strings. it worked somewhat better wrapped in a function
def ask_name():
    return [
        '\n[eliza] Hi my name is Eliza. What\'s your name?\n\n'
    ]


# type:         ask_QUESTION()
# input:        n/a
# output:       an array of possible "What's your major?" questions to ask
# description:  an array of strings. it worked somewhat better wrapped in a function
def ask_major():
    return [
        '\n[eliza] ' + name + ', that\'s right. I think I remember you from orientation. What is your major?\n\n',
        '\n[eliza] Hi ' + name + '. Tell me again what your major was.\n\n',
        '\n[eliza] Oh, ' + name + '. I knew it was something that started with ' + name[
                                                                                   :1] + '. What\'s your major?\n\n',
        '\n[eliza] Yeah, ' + name + '. I thought you looked familiar. What\'s your major?\n\n',
    ]


# type:         ask_QUESTION()
# input:        n/a
# output:       an array of possible "How are you liking your major?" questions to ask
# description:  an array of strings. it worked somewhat better wrapped in a function
def ask_feelings():
    return [
        '\n[eliza] So your major is ' + major + '? How are you liking it so far?\n\n',
    ]


# type:         ask_QUESTION()
# input:        n/a
# output:       an array of possible "Where are you from?" questions to ask
# description:  an array of strings. it worked somewhat better wrapped in a function
def ask_hometown():
    return [
        '\n[eliza] What is your hometown?\n\n',
        '\n[eliza] Where are you from?\n\n',
    ]


# type:         ask_QUESTION()
# input:        n/a
# output:       an array of possible "When do you expect to graduate?" questions to ask
# description:  an array of strings. it worked somewhat better wrapped in a function
def ask_gradyear():
    return [
        '\n[eliza] What year do you expect to graduate?\n\n',
        '\n[eliza] When do you think you\'ll graduate?\n\n',
    ]


# type:         ask_QUESTION()
# input:        n/a
# output:       an array of possible "Do you have any other questions for me?" questions to ask
# description:  an array of strings. it worked somewhat better wrapped in a function
def ask_other():
    return [
        '\n[eliza] Well if you didn\'t have any other questions then I guess I\'ll be on my way...\n\n',
        '\n[eliza] So I\'m assuming you don\'t have any other questions for me...\n\n',
    ]


# type:         respond_DERAILMENT()
# input:        n/a
# output:       an array of possible "Don't use that language!" statements to respond to swearing
# description:  an array of strings. it worked somewhat better wrapped in a function
def respond_swear():
    return [
        '\n[eliza] Hey! There\'s no need for that kind of language.\n\n',
        '\n[eliza] Please don\'t use profanity.\n\n',
        '\n[eliza] That is highly inappropriate.\n\n',
    ]


# type:         respond_DERAILMENT()
# input:        n/a
# output:       an array of possible "I don't understand you" statements to respond to gibberish
# description:  an array of strings. it worked somewhat better wrapped in a function
def respond_gibberish():
    return [
        '\n[eliza] I\'m sorry. I can\'t understand you.\n\n',
        '\n[eliza] Could you speak a little more clearly?\n\n',
        '\n[eliza] I\'m having difficulty interpreting what you\'re saying.\n\n',
    ]


# type:         respond_DERAILMENT()
# input:        n/a
# output:       an array of possible "What did you want to ask me?" questions to respond to question requests
# description:  an array of strings. it worked somewhat better wrapped in a function
def respond_question_request():
    return [
        '\n[eliza] Sure. What did you want to ask me?\n\n',
        '\n[eliza] What\'s your question\n\n',
    ]


# type:         respond_DERAILMENT()
# input:        a string of user input
# output:       an array of possible "Why do you ask x?" questions to respond to questions
# description:  an array of strings. it is made a little more complicated by scanning for specific types of questions.
#               if a user asks "How many x do I need", it responds "How many x do you think you need?"
def respond_question(user_in):
    responses = []

    # Generic response regardless of question type
    regex_total = r"^(.*[\.!,]\s)?((\bcan('?t)?\b)|(\bwould(n'?t)?\b)|(\bis(n'?t)?\b)|(\bare(n'?t)?\b)|(\bwill\b)|(" \
                  r"\bwon'?t\b)|(\bwho('?se?)?\b)|(\bwhat('?s)?\b)|(\bwhere('?s)?\b)|(\bwhen('?s)?\b)|(\bwhy\b)|(" \
                  r"\bhow\b)|(\bshould(n'?t)?\b)|(\bdo(n'?t)?\b))\s([^?\n]*)(\?)?$"

    # Why/where/when do/does/did questions
    regex_why_does = r"^(.*[\.!,]\s)?(\b(why|where|when|how)\s(do(es)?|did)\b)\s([^?\n]*)(\?)?$"

    # How much/many questions
    regex_how_many = r"^(.*[\.!,]\s)?(\bhow\s(many|much)\b)\s([^?\n]*)((\bi\b)|(\byou\b)|(\bs?he\b)|(\bthey\b))([" \
                     r"^?\n]*)(\?)?$"

    if re.match(regex_why_does, user_in, re.MULTILINE | re.IGNORECASE):
        subst = "\\3 do you think \\6?"
        statement = re.sub(regex_why_does, subst, pronoun_flip(user_in), 0, re.MULTILINE | re.IGNORECASE)
        responses.append('\n[eliza] ' + statement + '\n\n')
    elif re.match(regex_how_many, user_in, re.MULTILINE | re.IGNORECASE):
        subst = "How many \\4i think \\6\\10?"
        statement = pronoun_flip(re.sub(regex_how_many, subst, user_in, 0, re.MULTILINE | re.IGNORECASE)).capitalize()
        responses.append('\n[eliza] ' + statement + '\n\n')
    else:
        subst = "Why do you ask \\2 \\27?"
        responses.append(
            '\n[eliza] ' + re.sub(regex_total, subst, pronoun_flip(user_in), 0, re.MULTILINE | re.IGNORECASE) + '\n\n')

    return responses


# type:         respond_DERAILMENT()
# input:        n/a
# output:       an array of possible "Oh are you leaving?" questions to respond to requests to leave
# description:  an array of strings. it worked somewhat better wrapped in a function
#               *NOTE: User cannot actually say "no" to leaving. Once they have said "goodbye", Eliza shuts down
def respond_bye():
    return [
        '\n[eliza] Oh, are you leaving?\n\n',
        '\n[eliza] Is that all you needed?\n\n',
        '\n[eliza] Will that be all for today?\n\n',
    ]


# type:         respond_DERAILMENT()
# input:        n/a
# output:       an array of possible "It's okay" statements to respond to apologies
# description:  an array of strings. it worked somewhat better wrapped in a function
#               apologies may happen after user swears and Eliza shows annoyance
def respond_apology():
    return [
        '\n[eliza] It\'s okay\n\n',
        '\n[eliza] Apology accepted\n\n',
        '\n[eliza] You are forgiven\n\n',
    ]


# type:         respond_DERAILMENT()
# input:        n/a
# output:       an array of possible "Why don't you know?" questions to respond to uncertainty
# description:  an array of strings. it worked somewhat better wrapped in a function
def respond_unsure():
    return [
        '\n[eliza] You sound confused.\n\n',
        '\n[eliza] What don\'t you know?\n\n',
        '\n[eliza] Is there something I can clarify for you?\n\n',
    ]


# type:         respond_DERAILMENT()
# input:        n/a
# output:       an array of possible "Why are you x?/Why am I x?" questions to respond to declarations
# description:  an array of strings. it is made somewhat more complicated by scanning for regular expressions
#               statements like "I am happy" are replaced by "Why are you happy?"
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


# type:         respond_DERAILMENT()
# input:        n/a
# output:       an array of possible "Anyways..." statements to return to the topic at hand
# description:  an array of strings. it worked somewhat better wrapped in a function
def topic_change():
    return [
        '\n[eliza] Anyways, like I was saying...',
        '\n[eliza] So I don\'t think you actually answered this yet...',
        '\n[eliza] So getting back on topic...',
    ]


# type:         is_DISTRACTION()
# input:        a string of user input
# output:       whether or not the user is swearing
# description:  makes use of the Profanity Library for Python
def is_swearing(user_in):
    return profanity.contains_profanity(user_in)


# type:         is_DISTRACTION()
# input:        a string of user input
# output:       whether or not the user is speaking nonsense
# description:  uses a regular expression to see if any words do not contain vowels or if any letters are repeated
#               3 or more times. does not catch everything, but it catches stuff like "grrrr" or "ksjjhgfsdjhf"
def is_gibberish(user_in):
    regex = r"(((.*?)((^|[\n\t ])[^aeiouy\s\n0-9]+($|[\n\t ]))+(.*))|((.*?)(a{3,}|b{3,}|c{3,}|d{3,}|e{3,}|f{3,}|g{3," \
            r"}|h{3,}|i{3,}|j{3,}|k{3,}|l{3,}|m{3,}|n{3,}|o{3,}|p{3,}|q{3,}|r{3,}|s{3,}|t{3,}|u{3,}|v{3,}|w{3,}|x{3," \
            r"}|y{3,}|z{3,})(.*)))"
    if re.match(regex, user_in, re.MULTILINE | re.IGNORECASE):
        return True
    else:
        return False


# type:         is_DISTRACTION()
# input:        a string of user input
# output:       whether or not the user wants to ask a question
# description:  makes use of a regular expression to see if a user said the words "question" or "ask"
def is_question_request(user_in):
    regex = r".*\b(question|ask)\b.*"
    if re.match(regex, user_in, re.MULTILINE | re.IGNORECASE):
        return True
    else:
        return False


# type:         is_DISTRACTION()
# input:        a string of user input
# output:       whether or not the user is currently asking a question
# description:  makes use of a regular expression to see if a user said "who", "what", "when", etc. followed by content
def is_question(user_in):
    regex = r"^(.*[\.!,]\s)?((\bcan('?t)?\b)|(\bwould(n'?t)?\b)|(\bis(n'?t)?\b)|(\bare(n'?t)?\b)|(\bwill\b)|(" \
            r"\bwon'?t\b)|(\bwho('?se?)?\b)|(\bwhat('?s)?\b)|(\bwhere('?s)?\b)|(\bwhen('?s)?\b)|(\bwhy\b)|(\bhow\b)|(" \
            r"\bshould(n'?t)?\b)|(\bdo(n'?t)?\b))\s([^?\n]*)(\?)?$"
    if re.match(regex, user_in, re.MULTILINE | re.IGNORECASE):
        return True
    else:
        return False


# type:         is_DISTRACTION()
# input:        a string of user input
# output:       whether or not the user wants to leave
# description:  makes use of a regular expression to see if a user said the words "goodbye", "stop", etc.
def is_leaving(user_in):
    regex = r".*((\bgoodbye\b)|(\bfarewell\b)|(\bstop\b)|(\bexit\b)|(\bi'?m\sleaving\b)|(\b(to|will|gonna)\sleave\b)).*"
    if re.match(regex, user_in, re.MULTILINE | re.IGNORECASE):
        return True
    else:
        return False


# type:         is_DISTRACTION()
# input:        a string of user input
# output:       whether or not the user is apologizing
# description:  makes use of a regular expression to see if a user said the word "sorry"
def is_apologizing(user_in):
    regex = r".*\b(sorry)\b.*"
    if re.match(regex, user_in, re.MULTILINE | re.IGNORECASE):
        return True
    else:
        return False


# type:         is_DISTRACTION()
# input:        a string of user input
# output:       whether or not the user is declaring something
# description:  makes use of a regular expression to see if a user said something like "I am x" or "You are x"
def is_declaring(user_in):
    regex = r"^(.*[\.!?,]\s)?((\byou\b)|(\bi'?m?\b))(\s(\bam\b)|(\bare\b)|(\bis\b))?(.*)"
    if re.match(regex, user_in, re.MULTILINE | re.IGNORECASE):
        return True
    else:
        return False


# type:         is_DISTRACTION()
# input:        a string of user input
# output:       whether or not the user is confused
# description:  makes use of a regular expression to see if a user said they are unsure or don't know something
def is_unsure(user_in):
    regex = r".*\b(confused?|i\sdon'?t\sknow)\b.*"
    if re.match(regex, user_in, re.MULTILINE | re.IGNORECASE):
        return True
    else:
        return False


# type:         is_DISTRACTION()
# input:        a string of user input and whether an "I am" exception is allowed
# output:       whether or not the user is derailing the conversation
# description:  calls the other is_DISTRACTION() type functions and sees if any of them are active.
#               exceptions are made for things like "I am John" which would expect an "I am" style declaration
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


# type:         miscellaneous
# input:        an array of dialogue options
# output:       a string of the selected dialogue option
# description:  uses modulo division with a random starting point to cycle through responses
def randologue(option_array):
    global my_rand_int
    option = option_array[my_rand_int % len(option_array)]
    my_rand_int = my_rand_int + 1
    if my_rand_int > 19:
        my_rand_int = 20
    return option


# type:         miscellaneous
# input:        a string of user input and whether an "I am" exception is allowed
# output:       true user input (not derailed)
# description:  makes use of derailment detection to "force" the user to actually answer each question (unless they say
#               goodbye). while the user continues to be distracted, Eliza will remember where the conversation left
#               off by storing the dialogue array in the "options" variable. Users can be distracted for as long as
#               they wish, but eventually Eliza will say "Anyways, like I was saying..." and get back on topic
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


# type:         extract_INFORMATION()
# input:        a string of user input
# output:       the user's actual name stripped of all context
# description:  uses a regular expression to find out which word in the sentence is probably the first name
#               Statements like "I am x" or "My name is x" would return just "x"
def extract_name(test_str):
    regex = r"((.*\bmy\sname\sis\s)|(.*\bi\sam\s)|(.*\bi'?m\s)|(^\s))?(\S+)\b(.*)"
    subst = "\\6"
    result = re.sub(regex, subst, test_str, 0, re.MULTILINE | re.IGNORECASE).title()
    return result


# type:         extract_INFORMATION()
# input:        a string of user input
# output:       the user's actual major stripped of all context
# description:  uses a regular expression to find out which word in the sentence is probably the major
#               Statements like "It's x" or "I'm studying x" would return just "x"
def extract_major(test_str):
    regex = r"(^.*((\bis\b)|(\bwas\b)|(\bbe\b)|(\bit'?s\b)|(\bstudy(ing)?\b))\s)?(.*)"
    subst = "\\9"
    result = re.sub(regex, subst, test_str, 0, re.MULTILINE | re.IGNORECASE).title()
    return result


# type:         extract_INFORMATION()
# input:        a string of user input
# output:       the user's actual hometown stripped of all context
# description:  uses a regular expression to find out which word in the sentence is probably the hometown
#               Statements like "I am from x" or "I grew up in x" would return just "x"
def extract_hometown(test_str):
    regex = r"^((.*\bfrom\s\b)|(.*\bin\b\s))?(.*)"
    subst = "\\4"
    result = re.sub(regex, subst, test_str, 0, re.MULTILINE | re.IGNORECASE).title()
    return result


# type:         miscellaneous
# input:        n/a
# output:       the Eliza program
# description:  the main script of the program which calls all the other functions. the focus is preset dialogue but
#               always with the possibility of derailment
def main_script():
    global name, major
    print("This is Eliza the Academic Advisor, made by Jacob Schnoor")
    # print(pronoun_flip(input("Pronoun Flip: ")))
    name = extract_name(scan(ask_name(), True))
    major = extract_major(scan(ask_major(), True))
    feelings = scan(ask_feelings(), True)
    hometown = extract_hometown(scan(ask_hometown(), True))
    scan(ask_gradyear(), True)
    scan(["\n[eliza] What's your favorite color?\n\n"], False)
    scan(["\n[eliza] What's your favorite food?\n\n"], False)
    scan(["\n[eliza] Why did you decide to study " + major + "?\n\n"], False)
    scan(["\n[eliza] Are there a lot of " + major + " majors in " + hometown + "?\n\n"], False)
    scan(["\n[eliza] So " + name + ", earlier you described " + major + " by saying " + pronoun_flip(feelings) +
          ". Does that still hold true?\n\n"], False)
    scan((ask_other()), False)
    if name == 'Goodbye':
        print('\n[eliza] See ya')
    else:
        print('\n[eliza] It was nice talking to you, ' + name + '. Have a great rest of your day.')


# Merely calls the main_script() function to get the program running
main_script()
