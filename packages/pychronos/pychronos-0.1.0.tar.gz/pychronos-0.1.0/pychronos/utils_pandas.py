from typing import Text

import numpy as np
import pandas as pd

from openapi_client import SingleTimeSeriesData, RawSingleTimeSeriesData

from .dtype import DType

TIME_STORAGE_UNIT = 'us'  # data is stored in a database in microseconds

_chronos_freq_to_pandas = {
    "A": "A",
    "A-DEC": "A-DEC",
    "A-JAN": "A-JAN",
    "A-FEB": "A-FEB",
    "A-MAR": "A-MAR",
    "A-APR": "A-APR",
    "A-MAY": "A-MAY",
    "A-JUN": "A-JUN",
    "A-JUL": "A-JUL",
    "A-AUG": "A-AUG",
    "A-SEP": "A-SEP",
    "A-OCT": "A-OCT",
    "A-NOV": "A-NOV",

    "Q": "Q",
    "Q-JAN": "Q-JAN",
    "Q-FEB": "Q-FEB",
    "Q-MAR": "Q-MAR",
    "Q-APR": "Q-APR",
    "Q-MAY": "Q-MAY",
    "Q-JUN": "Q-JUN",
    "Q-JUL": "Q-JUL",
    "Q-AUG": "Q-AUG",
    "Q-SEP": "Q-SEP",
    "Q-OCT": "Q-OCT",
    "Q-NOV": "Q-NOV",

    "M": "M",

    "W": "W",
    "W-MON": "W-MON",
    "W-TUE": "W-TUE",
    "W-WED": "W-WED",
    "W-THU": "W-THU",
    "W-SAT": "W_SAT",

    "D": "D",
    "B": "B",
    "C": "C"
}

""" maps pandas freqstr to chronos Freq"""
_pandas_freq_to_chronos = {
    "A": "A",
    "A-DEC": "A",
    "A-JAN": "A-JAN",
    "A-FEB": "A-FEB",
    "A-MAR": "A-MAR",
    "A-APR": "A-APR",
    "A-MAY": "A-MAY",
    "A-JUN": "A-JUN",
    "A-JUL": "A-JUL",
    "A-AUG": "A-AUG",
    "A-SEP": "A-SEP",
    "A-OCT": "A-OCT",
    "A-NOV": "A-NOV",

    "Q": "Q",
    "Q-JAN": "Q-JAN",
    "Q-FEB": "Q-FEB",
    "Q-MAR": "Q-MAR",
    "Q-APR": "Q-APR",
    "Q-MAY": "Q-MAY",
    "Q-JUN": "Q-JUN",
    "Q-JUL": "Q-JUL",
    "Q-AUG": "Q-AUG",
    "Q-SEP": "Q-SEP",
    "Q-OCT": "Q-OCT",
    "Q-NOV": "Q-NOV",
    "Q-DEC": "Q",

    "M": "M",

    "W": "W",
    "W-MON": "W-MON",
    "W-TUE": "W-TUE",
    "W-WED": "W-WED",
    "W-THU": "W-THU",
    "W-SAT": "W_SAT",
    "W-SUN": "W",

    "D": "D",
    "B": "B",
    "C": "C"
}

_pandas_dtype_to_chronos = {
    'int64': 'int',
    'int32': 'int',
    'float64': 'float',
    'float32': 'float',
    'category': 'cat'
}


def chronos_freq_to_pandas(freq: Text):
    """
    convert chronos frequency to Pandas' frequency
    :param freq:
    :return:
    """
    if freq not in _chronos_freq_to_pandas.keys():
        raise ValueError(f"Invalid Chronos frequency,{freq}")

    return _chronos_freq_to_pandas[freq]


def pandas_index_to_chronos(index):
    """

    :param index: pnadas Index
    :return:
    """
    if isinstance(index, pd.PeriodIndex):
        # period
        if index.freq.freqstr not in _pandas_freq_to_chronos.keys():
            raise ValueError("Invalid Pandas frequency, %s" % index.freq.freqstr)
        return 'p', _pandas_freq_to_chronos[index.freq.freqstr], None

    elif isinstance(index, pd.DatetimeIndex):
        # time stamp
        if index.freq.freqstr not in _pandas_freq_to_chronos.keys():
            raise ValueError("Invalid Pandas frequency, %s" % index.freq.freqstr)
        return 't', _pandas_freq_to_chronos[index.freq.freqstr], None

    elif isinstance(index, (pd.Int64Index, pd.RangeIndex,)):
        # relative
        return 'r', None, None
    else:
        raise TypeError(f"Unsupported index, {index}")


def infer_chronos_dtype(data: pd.Series):
    if isinstance(data, pd.DataFrame):
        if len(data.columns) > 1:
            raise ValueError("DataFrame must have one column only")
    elif isinstance(data, pd.Series):
        pass
    elif isinstance(data, np.numarray):
        pass
    else:
        raise TypeError('unsupported input type')

    _dtype = data.dtype

    if isinstance(_dtype, pd.CategoricalDtype):
        return 'cat', {"categories": list(_dtype.categories), 'ordered': _dtype.ordered}

    elif isinstance(_dtype, np.dtype):
        if _dtype.type == np.float64:
            return "float", None

        elif _dtype.type in (np.int64, np.int32, np.int):
            return "int", None

        elif _dtype.type in (np.bool, np.bool_):
            return "bool", None

        elif _dtype.type in [np.object, np.object_, np.object0]:
            # figure out what is type without none
            _types = set([type(x) for x in data])
            # has None
            has_none = type(None) in _types
            if not has_none:
                raise TypeError('unsupported type')

            # other than None
            other_types = [x for x in _types if x is not type(None)]
            if len(other_types) > 1:
                raise TypeError('unsupported type')
            elif len(other_types) == 0:
                raise TypeError("cannot infer dtype from object with None only")

            if other_types[0] is type(True):
                return "bool", None
            else:
                raise TypeError('unsupported type')

        else:
            raise TypeError("unsupported dtype, %s" % _dtype.name)
    elif isinstance(_dtype, pd.Int64Dtype):
        return "int", None

    raise TypeError("unsupported type, %s" % _dtype)


def pandas_dtype_to_chronos(_dtype):
    """

    :param _dtype:
    :return:
    """
    if isinstance(_dtype, pd.CategoricalDtype):
        return 'cat', {"categories": list(_dtype.categories), 'ordered': _dtype.ordered}

    elif isinstance(_dtype, np.dtype):
        if _dtype.type == np.float64:
            return "float", None

        elif _dtype.type in (np.int64, np.int32, np.int):
            return "int", None

        elif _dtype.type in (np.bool, np.bool_):
            return "bool", None

        # elif _dtype == np.datetime
        # return 'datetime', {'unit': 'ns'}
        # elif _dtype.type == period

        elif _dtype.type in [np.object, np.object_, np.object0]:
            # figure out what is type without none
            raise NotImplementedError()

        else:
            raise TypeError("unsupported dtype, %s" % _dtype.name)
    elif isinstance(_dtype, pd.Int64Dtype):
        return "int", None

    raise TypeError("unsupported type, %s" % _dtype)


# Since many of these have platform-dependent definitions, a set of fixed-size aliases are provided:
#
# Numpy type                      C type          Description
# np.int8                         int8_t          Byte (-128 to 127)
# np.int16                        int16_t         Integer (-32768 to 32767)
# np.int32                        int32_t         Integer (-2147483648 to 2147483647)
# np.int64                        int64_t         Integer (-9223372036854775808 to 9223372036854775807)
# np.uint8                        uint8_t         Unsigned integer (0 to 255)
# np.uint16                       uint16_t        Unsigned integer (0 to 65535)
# np.uint32                       uint32_t        Unsigned integer (0 to 4294967295)
# np.uint64                       uint64_t        Unsigned integer (0 to 18446744073709551615)
# np.intp                         intptr_t        Integer used for indexing, typically the same as ssize_t
# np.uintp                        uintptr_t       Integer large enough to hold a pointer
# np.float32                      float
# np.float64 / np.float_          double          Note that this matches the precision of the builtin python float.
# np.complex64                    float complex   Complex number, represented by two 32-bit floats (real and imaginary components)
# np.complex128 / np.complex_     double complex  Note that this matches the precision of the builtin python complex.
#

def index_value_to_pandas_period_value(inx, freq: str):
    """
    used to convert to index in epoch format to pandas Period/Datetime

    :param freq: value from Freq.values
    :param inx: integer
    :return: pd.Period, pd.DateTime, np.datetime64
    """

    return pd.Timestamp(inx, freq=freq, unit=TIME_STORAGE_UNIT).to_period()


def pandas_time_to_index(inx, date_format=TIME_STORAGE_UNIT):
    """
    used to convert pandas period/Datetime to index in epoch format

    :param inx: pd.Period, pd.DateTime, np.datetime64
    :param date_format: iso, s, ms, us, ns
    :return:
    """

    if isinstance(inx, pd.Period):
        # return t.end_time
        # return inx.to_timestamp()
        if date_format == 'iso':
            return inx.to_timestamp().isoformat()
        else:
            tmp = inx.to_timestamp().to_datetime64().astype(int)

    elif isinstance(inx, pd.Timestamp):
        if date_format == 'iso':
            return inx.isoformat()
        else:
            tmp = inx.to_datetime64().astype(int)

    else:
        raise ValueError("invalid index value")

    if date_format == "s":
        return int(tmp / 10 ** 9)
    elif date_format == "ms":
        return int(tmp / 10 ** 6)
    elif date_format == "us":
        return int(tmp / 10 ** 3)
    elif date_format == "ns":
        return tmp
    else:
        raise ValueError("unknown date_format {}".format(date_format))


def values_to_pandas_values(values, dtype, dparams):
    """converts values to pandas"""
    if dtype == "cat":
        tmp = pd.Categorical(values=values, categories=dparams.get('categories'), ordered=dparams.get('ordered'))
        return tmp, tmp.dtype
    elif dtype == "int":
        # if any value is NaN then use Int64 type instead of int !!!
        if pd.isna(values).any():
            return [np.nan if x is None else np.int64(x) for x in values], pd.Int64Dtype()
        else:
            return np.array(values), 'int'
    elif dtype == "float":
        return values, 'float'
    elif dtype == "bool":
        if pd.isna(values).any():
            return values, 'object'
        else:
            return values, 'bool'
    else:
        raise TypeError(f"unsupported data type from the server, {dtype}")


def pandas_values_to_chronos_values(data, dtype):
    """
    converts values to pandas

    """
    if data.dtype == np.int64:
        return data.tolist()

    if data.dtype == np.float64:
        return data.tolist()

    elif isinstance(data.dtype, pd.Int64Dtype):
        return [None if x is np.nan else int(x) for x in data]

    elif isinstance(data.dtype, pd.CategoricalDtype):
        return data.tolist()

    elif data.dtype == bool:
        return data.tolist()

    elif data.dtype == object and dtype == DType.bool.value:
        return data.tolist()

    else:
        raise TypeError(f"unsupported data type, {data.dtype}")


def singleTimeSeriesData_to_series(data):
    """
    converts server response to panda
    :param data:
    :return:
    """
    if not isinstance(data, SingleTimeSeriesData):
        raise TypeError("data must be SingleTimeSeriesData")

    if data.format == "split":
        index = [index_value_to_pandas_period_value(x, freq=chronos_freq_to_pandas(data.freq)) for x in data.index]
        values, dtype = values_to_pandas_values(data.values, dtype=data.dtype, dparams=data.dparams)
        status = data.status
        return pd.Series(values, index=index, dtype=dtype)

    elif data.format == 'obs':
        raise NotImplementedError
    else:
        raise ValueError('unsupported format, {}'.format(data.format))


def rawSingleTimeSeriesData_to_series(data: RawSingleTimeSeriesData):
    """
    converts server response to panda
    :param data:
    :return:
    """
    if not isinstance(data, RawSingleTimeSeriesData):
        raise TypeError("data must be RawSingleTimeSeriesData")

    index = [index_value_to_pandas_period_value(x, freq=chronos_freq_to_pandas(data.freq)) for x in data.index] \
        if data.index else []
    values, dtype = values_to_pandas_values(data.values, dtype=data.dtype, dparams=data.dparams)
    status = data.status
    return pd.Series(data=values, index=index, name=data.name, dtype=dtype)


def series_to_SingleTimeSeriesData(data, tsid, coll_id) -> SingleTimeSeriesData:
    """
    converts server response to panda
    :param coll_id:
    :param tsid:
    :param data:
    :return:
    """
    if not isinstance(data, pd.Series):
        raise TypeError("must be panda Series")

    itype, freq, fparams = pandas_index_to_chronos(data.index)
    # dtype, dparams = pandas_dtype_to_chronos(data.dtype)
    dtype, dparams = infer_chronos_dtype(data)

    return SingleTimeSeriesData(
        name=data.name,
        tsid=str(tsid),
        coll_id=str(coll_id),
        format="split",
        index_format='us',
        values=pandas_values_to_chronos_values(data.values, dtype),  # data.values.tolist(),
        index=[pandas_time_to_index(x, date_format='us') for x in data.index],
        nobs=len(data),
        status=None,
        itype=itype,
        freq=freq,
        dtype=dtype,
        dparams=dparams

    )


def series_to_RawSingleTimeSeriesData(data, tsid, coll_id):
    """
    converts server response to panda
    :param coll_id:
    :param tsid:
    :param data:
    :return:
    """
    if not isinstance(data, pd.Series):
        raise TypeError("must be panda Series")

    itype, freq, fparams = pandas_index_to_chronos(data.index)
    # dtype, dparams = pandas_dtype_to_chronos(data.dtype)
    dtype, dparams = infer_chronos_dtype(data)

    return RawSingleTimeSeriesData(
        name=data.name,
        tsid=str(tsid),
        coll_id=str(coll_id),
        index_format='us',
        values=pandas_values_to_chronos_values(data.values, dtype),
        index=[pandas_time_to_index(x, date_format='us') for x in data.index],
        nobs=len(data),
        status=None,
        itype=itype,
        freq=freq,
        dtype=dtype,
        dparams=dparams
    )
