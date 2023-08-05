__version__ = "0.2.0"

import hashlib
from collections import Counter
from re import findall
from string import punctuation

import requests


def check_password(password: str) -> int:
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest()

    response = requests.get(f"https://api.pwnedpasswords.com/range/{sha1[:5]}")

    hash_suffix_list = [x.split(":") for x in response.text.splitlines(False)]

    try:
        count = [count for suffix,
                 count in hash_suffix_list if sha1.endswith(suffix.lower())][0]
    except IndexError:
        return 0

    return int(count)


class PasswordRequirements:
    def __init__(self, *, min_length: int = 0, min_digits: int = 0, min_special: int = 0):
        self.min_length = min_length
        self.min_digits = min_digits
        self.min_special = min_special

    def check(self, password: str):
        if len(password) < self.min_length:
            return False

        digits = len(findall(r"\d", password))
        if digits < self.min_digits:
            return False

        special_chars = sum(v for k, v in Counter(password).items() if k in punctuation)
        if special_chars < self.min_special:
            return False

        return True
