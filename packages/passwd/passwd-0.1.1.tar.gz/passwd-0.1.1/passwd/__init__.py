__version__ = "0.1.1"

import hashlib

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
