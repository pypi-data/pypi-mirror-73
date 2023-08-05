__version__ = "0.3.0"

import hashlib
from collections import Counter
from re import findall
from string import punctuation, ascii_letters, ascii_uppercase, ascii_lowercase

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
    def __init__(self, *, min_length: int = 0, min_digits: int = 0, min_special: int = 0, min_alpha: int = 0, min_upper: int = 0, min_lower: int = 0):
        self.min_length = min_length
        self.min_digits = min_digits
        self.min_special = min_special
        self.min_alpha = min_alpha
        self.min_upper = min_upper
        self.min_lower = min_lower

    def check(self, password: str):
        if len(password) < self.min_length:
            return False

        digits = len(findall(r"\d", password))
        if digits < self.min_digits:
            return False

        special_chars = sum(v for k, v in Counter(password).items() if k in punctuation)
        if special_chars < self.min_special:
            return False
        
        alpha_chars = sum(v for k, v in Counter(password).items() if k in ascii_letters)
        if alpha_chars < self.min_alpha:
            return False
        
        upper_chars = sum(v for k, v in Counter(password).items() if k in ascii_uppercase)
        if upper_chars < self.min_upper:
            return False
        
        lower_chars = sum(v for k, v in Counter(password).items() if k in ascii_lowercase)
        if lower_chars < self.min_lower:
            return False
        
        return True
