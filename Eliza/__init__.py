# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

regex = r"(?:(?:I|you|he|she|they|we|it)(?:.*)\s(?:know|think|feel|seem)s?(?:\sthat\s)?(?:\slike\s)?)?(.*)\bme\b([^!\.?\n]*)(.*)$"

test_str = input('Why did you come here today?\n'.upper())

subst = "Why do you feel like \\1you\\2?"

# You can manually specify the number of replacements by changing the 4th argument
result = re.sub(regex, subst, test_str, 0, re.MULTILINE | re.IGNORECASE)

if result:
    print(result.upper())

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.
