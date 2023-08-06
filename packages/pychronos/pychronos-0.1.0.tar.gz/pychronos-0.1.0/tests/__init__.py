import random
from datetime import datetime

import pandas as pd


def makePeriodIndex(k=10, name=None, freq="B", start: datetime = None, **kwargs):
    if start is None:
        start = datetime(2000, 1, 1)
    return pd.period_range(start=start, periods=k, freq=freq, name=name, **kwargs)


def makePeriodSeries(nper=10, name=None, freq="B", dtype="int64", start=None):
    if dtype == "int64":
        data = [random.randint(0, 100) for i in range(nper)]
    elif dtype == "float64":
        data = random.randn(nper)
    elif dtype == 'bool':
        data = random.randn(nper) < 0
    elif dtype == 'categorical':
        cat = {0: "zero", 1: "one", 2: "two"}
        data = pd.Categorical([random.randint(0, 3) for i in range(10)],
                              categories=cat, ordered=True)
    else:
        raise ValueError("unsupported dtype, {}".format(dtype))

    return pd.Series(data, index=makePeriodIndex(nper, freq=freq, start=start), name=name)
