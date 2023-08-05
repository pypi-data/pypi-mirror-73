# -*- coding: utf-8 -*-
from . import helpers
from collections import Counter

def count_token(text):
    """Counts token size"""
    return len(text)


def get_bigram(text):
    """Counts N-gram"""
    cur = '[BOS]'
    bigrams = []
    for token in text:
        pre = cur
        cur = token
        bigrams.append((pre, cur))

    return bigrams

def get_bigram_frequency(text):
    """Get"""
    cur = '[BOS]'
    bigrams = []
    for token in text:
        pre = cur
        cur = token
        bigrams.append((pre, cur))

    frequencies = Counter(bigrams)

    return frequencies
