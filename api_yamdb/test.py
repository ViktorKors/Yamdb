import re
from django.core.exceptions import ValidationError

import regex

# regex.match(r'^[\w.@+-]+\z', "Latin text")

def username_reguar2(value):
    pattern = '^[\w.@+-]+\z'
    result = re.search(r'^[\w.@+-]', value)
    if result:
        print("YES! We have a match!")
    else:
      print("No match")


def username_reguar3(value):
    pattern = '^[\w.@+-]+\z'
    if re.search(r'^[\w.@+-]', value) is None:
        raise ValidationError(
            (f'Не допустимые символы <{value}> в нике.'),
            params={'value': value},
        )

def username_reguar(value):
    # pattern = '^[\w.@+-]+\z'
    result = re.search(r'^[\\w.@+-]+\\z', value)
    if not result:
        raise ValidationError(
            "Придумайте другой никнэйм"
        )

username_reguar("|-|aTa|_|_|a")

# print(re.fullmatch(r'^[\w.@+-]', 'fgdf'))

# print(re.search(r'^[\w.@+-]', 'fgdf'))


# txt = "fgdf"
# x = re.search("^[\w.@+-]", txt)
# if x:
#   print("YES! We have a match!")
# else:
#   print("No match")