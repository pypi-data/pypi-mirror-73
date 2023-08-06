from enum import Enum
import numpy as np

numpy_to_chronos = {
    'int64': 'int64',
    'int32': 'int64',
    'float64': 'float64',
    'float32': 'float32',
    'bool': 'bool'
}


class DType(Enum):
    int64 = 'int'
    float64 = 'float'
    bool = 'bool'
    categorical = 'cat'
    datetime = 'datetime'
    period = 'period'

    @staticmethod
    def keys():
        return [name for name, _ in DType.__members__.items()]

    @staticmethod
    def values():
        return [val.value for _, val in DType.__members__.items()]

    @staticmethod
    def from_pandas(obj):
        if not hasattr(obj,"dtype"):
            raise ValueError

        if not isinstance(obj.dtype, np.dtype):
            raise ValueError

        return DType(numpy_to_chronos[obj.dtype.name])


all_dtypes_abbriviations = DType.values()

