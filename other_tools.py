"""
from stack overflow https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
"""


def make_ordinal(value):
    ordinal = lambda n: "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])
    return str(ordinal(value))
