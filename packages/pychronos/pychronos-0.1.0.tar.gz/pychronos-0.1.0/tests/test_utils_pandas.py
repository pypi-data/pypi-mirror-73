import json
import unittest
import pandas as pd
import numpy as np
from pychronos.utils_pandas import pandas_values_to_chronos_values, pandas_dtype_to_chronos, pandas_index_to_chronos, \
    infer_chronos_dtype


# from pandas.core.dtypes.common import is_object_dtype
# from utils_pandas import pandas_dtype_to_chronos, pandas_index_to_chronos


class DTypeTest(unittest.TestCase):

    def test_float(self):
        s = pd.Series([1.2321321, 4234234234.234, 10.12312 ** 34])
        dtype, dparams = pandas_dtype_to_chronos(s.dtype)
        self.assertEqual(np.float64, s.dtype)
        self.assertEqual('float', dtype)
        self.assertIsNone(dparams)

    def test_bool(self):
        s = pd.Series([False, True, False, True])
        # dtype, dparams = pandas_dtype_to_chronos(s.dtype)
        dtype, dparams = infer_chronos_dtype(s)

        self.assertEqual('bool', dtype)
        self.assertIsNone(dparams)

    def test_categorical(self):
        # unordered
        vertebrate_types = ['Mammal', 'Reptile', 'Bird', 'Amphibian', 'Fish']
        s = pd.Series(
            pd.Categorical(['Mammal', 'Bird', 'Amphibian', 'Fish', 'Mammal', 'Fish'], categories=vertebrate_types))

        dtype, dparams = infer_chronos_dtype(s)
        self.assertEqual('cat', dtype)
        self.assertFalse(dparams['ordered'])
        self.assertEqual(dparams['categories'], list(s.dtype.categories))

        # s.values.codes
        # s.values.categories
        # s.values.ordered

        # ordered
        ordered_satisfaction = ['Very Unhappy', 'Unhappy', 'Neutral', 'Happy', 'Very Happy']
        s = pd.Series(
            pd.Categorical(['Mad', 'Happy', 'Unhappy', 'Neutral'], ordered=True, categories=ordered_satisfaction))

        dtype, dparams = pandas_dtype_to_chronos(s.dtype)
        self.assertEqual('cat', dtype)
        self.assertTrue(dparams['ordered'])
        self.assertEqual(ordered_satisfaction, dparams['categories'])

    def test_integer(self):
        s = pd.Series([1, 2, 3, 4])
        dtype, dparams = infer_chronos_dtype(s)
        self.assertEqual(np.int64, s.dtype)
        self.assertEqual('int', dtype)
        self.assertIsNone(dparams)

    def test_mixed_dtypes(self):
        s = pd.Series([123, True, False, True])
        with self.assertRaises(TypeError):
            dtype, dparams = infer_chronos_dtype(s)

        s = pd.Series([213.213, 21.213, 10 ** 34])
        with self.assertRaises(TypeError):
            dtype, dparams = infer_chronos_dtype(s)

        s = pd.Series([213.213, 21.213, "sadas"])
        with self.assertRaises(TypeError):
            dtype, dparams = infer_chronos_dtype(s)

    def test_period(self):
        s = pd.Series([213.213, 21.213, 12.23], index=pd.period_range(start="2010-01-01", periods=3, freq="Q"))
        itype, freq, fparams = pandas_index_to_chronos(s.index)
        self.assertEqual('p', itype)
        self.assertEqual('Q', freq)
        self.assertIsNone(fparams)

    def test_IntIndex(self):
        s = pd.Series([213.213, 21.213, "sadas"], index=[0, 21, 100])
        itype, freq, fparams = pandas_index_to_chronos(s.index)
        self.assertEqual('r', itype)
        self.assertIsNone(freq)
        self.assertIsNone(fparams)

        s = pd.Series([213.213, 21.213, "sadas"], index=pd.RangeIndex(start=0, stop=3))
        itype, freq, fparams = pandas_index_to_chronos(s.index)
        self.assertEqual('r', itype)
        self.assertIsNone(freq)
        self.assertIsNone(fparams)

    def test_unsupportedIndices(self):
        s = pd.Series([213.213, 21.213, "sadas"], index=pd.CategoricalIndex(['a', 'b', 'c']))
        with self.assertRaises(TypeError):
            type, freq, fparams = pandas_index_to_chronos(s.dtype)

        s = pd.Series([213.213, 21.213, "sadas"], index=pd.interval_range(start=0, end=3))
        with self.assertRaises(TypeError):
            type, freq, fparams = pandas_index_to_chronos(s.dtype)

        s = pd.Series([213.213, 21.213, "sadas"], index=pd.MultiIndex.from_arrays([[1, 1, 2], ['red', 'blue', 'red']],
                                                                                  names=('number', 'color')))
        with self.assertRaises(TypeError):
            type, freq, fparams = pandas_index_to_chronos(s.dtype)


    def test_pandas_values_to_chronos_values_Int(self):

        # given
        orig = [213, 21, 10000000000]

        # when
        ps = pd.Series(orig, index=pd.period_range("2010-01-01", periods=3))

        self.assertEqual(ps.dtype, np.int64)

        dtype, dparams = infer_chronos_dtype(ps)

        values = pandas_values_to_chronos_values(ps, dtype)

        txt = json.dumps(values)
        values2 = json.loads(txt)

        # then
        self.assertEqual(orig, values2)

    def test_pandas_values_to_chronos_values_float(self):

        # given
        orig = [2133432432432423.4, 2.1, 0.00000000000000000000001]

        # when
        ps = pd.Series(orig, index=pd.period_range("2010-01-01", periods=3))

        self.assertEqual(ps.dtype, np.float64)

        dtype, dparams = infer_chronos_dtype(ps)

        values = pandas_values_to_chronos_values(ps, dtype)

        txt = json.dumps(values)
        values2 = json.loads(txt)

        # then
        self.assertEqual(orig, values2)

    def test_pandas_values_to_chronos_values_bool(self):

        # given
        orig = [True, False, True]

        # when
        ps = pd.Series(orig, index=pd.period_range("2010-01-01", periods=3))

        self.assertEqual(ps.dtype, np.bool)

        dtype, dparams = infer_chronos_dtype(ps)

        values = pandas_values_to_chronos_values(ps, dtype)

        txt = json.dumps(values)
        values2 = json.loads(txt)

        # then
        self.assertEqual(orig, values2)

    def test_pandas_values_to_chronos_values_categorical(self):
        # given
        N = 5
        orig = pd.Categorical(['a', 'b', 'c', 'a', 'd'], ordered=True, categories=['c', 'b', 'a'])

        # when
        ps = pd.Series(orig, index=pd.period_range('1950-01', periods=N, freq='Q'))

        self.assertIsInstance(ps.dtype, pd.CategoricalDtype)

        dtype, dparams = infer_chronos_dtype(ps)

        values = pandas_values_to_chronos_values(ps, dtype)

        txt = json.dumps(values)
        values2 = json.loads(txt)

        # then
        self.assertTrue(orig.equals(pd.Categorical(values2, ordered=True, categories=['c', 'b', 'a'])))






