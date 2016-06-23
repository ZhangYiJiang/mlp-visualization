import re
from urllib.parse import urlparse


def remove_special(s):
    return re.sub(r"[?|:*/\\<>\"]+", '', s)


def flatten(lst):
    return [a for b in lst for a in b]


def intersect(a, b):
    for i in a:
        if i in b:
            return True
    return False


def word_count(s):
    return s.count(' ') + s.count('\n') + 1


def freq(lst):
    tbl = {}

    for i in lst:
        tbl[i] = tbl.get(i, 0) + 1

    return tbl


def sort_dict(d):
    return sorted(d.items(), key=lambda l: l[1], reverse=True)


def is_absolute(url) -> bool:
    return bool(urlparse(url).netloc)


def identity(*args):
    if len(args) == 1:
        return args[0]
    return args


def sluggify(s):
    return re.sub(r"[\W]+", '-', s.lower(), flags=re.ASCII)


def deep_flatten(lst):
    if not isinstance(lst, list):
        return [lst]
    ret = []
    for i in lst:
        ret.extend(deep_flatten(i))
    return ret
