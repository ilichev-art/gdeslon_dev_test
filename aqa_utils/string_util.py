import re
import random
import string


class StringUtil:

    @staticmethod
    def get_first_string_or_default(def_val, *args):
        return next((s for s in args if s), def_val)

    @staticmethod
    def get_first_match_by_regex(pattern, content):
        match = re.search(pattern, content)
        if match:
            return match.group(1)
        return ""

    @staticmethod
    def get_random_string(min_length=3, max_length=10):
        return ''.join(random.choices(string.ascii_letters, k=random.randint(min_length, max_length)))

    @staticmethod
    def get_random_int_string(min_length=3, max_length=10):
        return ''.join(random.choices(string.digits, k=random.randint(min_length, max_length)))
