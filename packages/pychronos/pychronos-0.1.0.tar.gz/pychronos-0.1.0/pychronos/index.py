from datetime import datetime
from enum import Enum as BasicEnum

class Enum(BasicEnum):

    @classmethod
    def values(cls):
        return [x.value for x in cls]

    @classmethod
    def keys(cls):
        return [x.name for x in cls]

"""
Unix timestamp is # of second from epoch
Mongodb Timestamp (64bits) is # of millisecond (10^3) from epoch
Postgres Timestamp (64bits)is # of microsecond (10^6) from epoch
Numpy Timestamp (datetime64, 64bits)is # of nanosecond (10-9) from epoch

ChronosDB stores time in microseconds in 64bit integer from epoch.

Real time (valid time) is stored in milliseconds (10^3). This is mainly to limitation of MongoDB, which timestamp has
precision of millisecond only.

"""


class IType(Enum):
    period = "p"
    timestamp = "t"
    relative = "r"
    integer = 'i'


index_types = IType.values()


def index_value_to_db_index_value(v, _in="us"):
    """ converts from us any raw input format to (microseconds)"""
    if _in == "us":
        return v
    elif _in == 's':
        return v * (10 ** 6)
    elif _in == "ms":
        return v * (10 * 3)
    elif _in == "ns":
        return int(v / (10 ** 3))


def index_to_db_index(inx, _in="us"):
    """
    this may have to be changed to numpy array
    """
    if _in == "us":
        return inx
    elif _in == 's':
        return [v * (10 ** 6) for v in inx]
    elif _in == "ms":
        return [v * (10 * 3) for v in inx]
    elif _in == "ns":
        return [int(v / (10 ** 3)) for v in inx]


def epoch64_to_datetime(i):
    return datetime.datetime.fromtimestamp(i / 10 ** 9)


def datetime_to_epoch64(dt):
    return int(dt.timestamp() * 10 ** 6) * 10 ** 3
