# stdlib
import hashlib


def fix_value_string(text: str) -> str:
    t = text
    dot_pos = t.rfind(".")
    comma_pos = t.rfind(",")
    if comma_pos > dot_pos:
        t = t.replace(".", "")
        t = t.replace(",", ".")
    else:
        t = t.replace(",", "")
    return t


def hash_string(s: str) -> str:
    h = hashlib.md5(s.encode("utf-8")).hexdigest()
    return h
