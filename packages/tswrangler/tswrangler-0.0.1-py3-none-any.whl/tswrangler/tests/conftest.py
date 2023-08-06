import functools
import random

import numpy as np
import pandas as pd
import pytest

np.random.seed([50])


def gen_avg(expected_avg=1, n=50, min_=0.9, max_=1.1):
    """
    Generates a random number list with known average.
    Taken from: https://stackoverflow.com/a/39435600/4032552
    """
    while True:
        l = [random.randint(min_, max_) for i in range(n)]
        avg = functools.reduce(lambda x, y: x + y, l) / len(l)

        if avg == expected_avg:
            return l


@pytest.fixture()
def continuous_timeseries():
    index = pd.date_range(start='1/1/2015', end='1/01/2020')
    price = np.random.randn(len(index))
    return pd.DataFrame(data=price, index=index, columns=["price"])
