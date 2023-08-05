# -*- coding: utf-8 -*-
from . import helpers
from collections import Counter
import numpy as np

def team_wake(text):
    """Counts token size"""
    members = np.array([
            '近田さん',
            '和食さん',
            '松井さん',
            '木田さん',
            '親分',
            '上田さん',
            '大塚さん',
            '村田さん',
            '伊藤さん',
            '高階さん',
            '澤田さん',
            '山田さん',
            '狩野さん',
            '石川さん',
            '後藤さん',
            '兼本さん',
            '佐藤さん',
            '五十嵐',
    ])
    shuhins = np.array([
            '安田さん',
            '小澤さん',
            '熊沢さん',
        ])
    np.random.shuffle(members)
    res = np.split(members, 3)

    return [mems, shuhin for mems, shuhin in zip(res, shuhins)]

