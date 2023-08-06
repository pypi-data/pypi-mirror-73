import random
import time
import unittest

import numpy as np
import pandas as pd

import pychronos
import pychronos.init
from pychronos import Freq, IType
from pychronos.dtype import DType

HOST = "http://localhost"
PORT = 9090


# HOST = "https://tshub-dev.appspot.com"
# PORT = 443


class TimeSeriesTest(unittest.TestCase):

    def setUp(self):

        self.space_name = "test_space"
        self.coll_name = "test_collection"

        self.chronos = pychronos.init(username="testuser", password="Testpass1!", host=HOST, port=PORT)

        if self.space_name in self.chronos.list_spaces():
            self.space = self.chronos[self.space_name]
            self.space.delete()

        self.space = self.chronos.create(self.space_name)

        if self.coll_name in self.space.list_collections():
            coll = self.space[self.coll_name]
            coll.delete()

        self.coll = self.space.create(self.coll_name)

    def tearDown(self):
        try:
            self.space = self.chronos[self.space_name]
            self.space.delete()
        except:
            pass

    def create_ts(self, name, itype=IType.period, freq="Q", dtype="int", **kwargs):

        if name in self.coll.list_timeseries():
            self.coll[name].delete()

        return self.coll.create(name, itype=itype, freq=freq, dtype=dtype, **kwargs)

    def test_create(self):
        ts_name = "x"
        if ts_name in self.coll.list_timeseries():
            self.coll[ts_name].delete()

        self.coll.create(ts_name, "Q", "int")

        self.assertIn(ts_name, self.coll.list_timeseries())
        ts = self.coll[ts_name]
        self.assertEqual("Q", ts.freq)
        self.assertEqual(DType.int64.value, ts.dtype)

    def test_update_rename(self):
        ts_name = "x"
        self.create_ts(ts_name)

        self.assertIn(ts_name, self.coll.list_timeseries())
        ts = self.coll[ts_name]
        ts.name = "y"
        self.assertIn("y", self.coll.list_timeseries())
        self.assertNotIn(ts_name, self.coll.list_timeseries())

    def test_update_title(self):
        ts_name = "x"
        ts_title = "title"
        self.create_ts(ts_name, title=ts_title)

        self.assertIn(ts_name, self.coll.list_timeseries())
        ts = self.coll[ts_name]
        self.assertEqual(ts_title, ts.title)

        ts.title = "new title"

        ts2 = self.coll[ts_name]
        self.assertEqual("new title", ts2.title)

    def test_update_descritpion(self):
        ts_name = "x"
        description = "description"
        self.create_ts(ts_name, description=description)

        self.assertIn(ts_name, self.coll.list_timeseries())
        ts = self.coll[ts_name]
        self.assertEqual(description, ts.description)

        ts.description = "new description"

        ts2 = self.coll[ts_name]
        self.assertEqual("new description", ts2.description)

    def test_attributes(self):
        """ """
        ts = self.coll.create(name="xyz", freq="Q", dtype="int")
        self.assertIsNone(ts.attributes)
        ts.attributes = {"xyz": 1234, "y": "dsfdsa"}

        ts2 = self.coll['xyz']
        self.assertEqual({"xyz": 1234, "y": "dsfdsa"}, ts2.attributes)

        ts2.attributes = {"y": 1234}
        ts3 = self.coll['xyz']
        self.assertEqual({"y": 1234}, ts3.attributes)

    def test_delete(self):
        ts_name = "x"
        ts = self.create_ts(ts_name)
        self.assertIn(ts_name, self.coll.list_timeseries())

        ts.delete()

        self.assertNotIn(ts_name, self.coll.list_timeseries())
        self.assertIsNone(ts.name)

    def test_save_pandas(self):
        # save pandas
        ts = self.coll.create("xyz", "Q", DType.int64)

        pts_time = pd.period_range('1950-01', periods=5, freq='Q')
        val = range(0, 5)
        x = pd.Series(val, index=pts_time)
        ts.save(x)

        # retrieve
        xx = ts.get()
        self.assertTrue(x.equals(xx))

    def test_save_append_overlapping(self):
        """
        appends new values only, this will generate error if some period are overwritten
        :return:
        """
        ts = self.coll.create("xyz", "Q", DType.int64)

        pts_time = pd.period_range('1950-01', periods=2, freq='Q')
        val = range(0, 2)
        x = pd.Series(val, index=pts_time)
        ts.save(x)

        pts_time = pd.period_range('1950-04', periods=2, freq='Q')
        val = range(10, 12)
        xx = pd.Series(val, index=pts_time)

        # append
        v = ts.save(xx, method='append')

        # check
        y = ts.get()
        self.assertEqual(0, y[0])
        self.assertEqual(1, y[1])  # value wasn't overwritten
        self.assertEqual(11, y[2])

    def test_save_append_nonoverlapping(self):
        """
        appends new values only, this will generate error if some period are overwritten
        :return:
        """
        ts = self.coll.create("xyz", "Q", DType.int64)

        pts_time = pd.period_range('1950-1', periods=2, freq='Q')
        val = range(0, 2)
        x = pd.Series(val, index=pts_time)
        ts.save(x)

        pts_time = pd.period_range('1951-1', periods=2, freq='Q')
        val = range(10, 12)
        xx = pd.Series(val, index=pts_time)

        # append
        v = ts.save(xx, method='append')

        # check
        y = ts.get()
        self.assertTrue(y.equals(x.append(xx)))

    def test_save_append_prepend(self):
        """
        appends new values only with index before the existing values
        :return:
        """
        ts = self.coll.create("xyz", "Q", DType.int64)

        pts_time = pd.period_range('1951-1', periods=2, freq='Q')
        val = range(0, 2)
        x = pd.Series(val, index=pts_time)
        ts.save(x)

        pts_time = pd.period_range('1950-1', periods=2, freq='Q')
        val = range(10, 12)
        xx = pd.Series(val, index=pts_time)

        # append
        v = ts.save(xx, method='append')

        # check
        y = ts.get()
        self.assertTrue(y.equals(xx.append(x)))

    def test_save_append_within(self):
        """
        appends new values only
        :return:
        """
        ts = self.coll.create("xyz", "Q", DType.int64)

        pts_time = pd.period_range('1950-1', periods=4, freq='Q')
        val = range(0, 4)
        x = pd.Series(val, index=pts_time)
        ts.save(x)

        pts_time = pd.period_range('1950-2', periods=2, freq='Q')
        val = range(10, 12)
        xx = pd.Series(val, index=pts_time)

        # append
        v = ts.save(xx, method='append')
        # nothing was written
        self.assertIsNone(v)

        # check
        y = ts.get()
        self.assertTrue(x.equals(y))

    def test_save_update(self):
        """
        update existing values or
        :return:
        """
        ts = self.coll.create("xyz", "Q", DType.int64)

        pts_time = pd.period_range('1950-01', periods=2, freq='Q')
        val = range(0, 2)
        x = pd.Series(val, index=pts_time)
        ts.save(x)

        pts_time = pd.period_range('1950-04', periods=2, freq='Q')
        val = range(10, 12)
        xx = pd.Series(val, index=pts_time)

        # append
        v = ts.save(xx, method='update')

        # check
        y = ts.get()
        self.assertEqual(0, y[0])
        self.assertEqual(10, y[1])  # value was overwritten
        self.assertEqual(11, y[2])

    def test_save_overwrite(self):
        """
        existing values all erased and data is written from scratch

        :return:
        """
        ts = self.coll.create("xyz", "Q", DType.int64)

        pts_time = pd.period_range('1950-01', periods=2, freq='Q')
        val = range(0, 2)
        x = pd.Series(val, index=pts_time)
        ts.save(x)

        pts_time = pd.period_range('1950-04', periods=2, freq='Q')
        val = range(10, 12)
        xx = pd.Series(val, index=pts_time)

        # append
        v = ts.save(xx, method='overwrite')

        # check
        y = ts.get()
        self.assertTrue(y.equals(xx))

    def test_get_empty_ts_data(self):
        ts = self.coll.create("xyz", "Q", DType.int64)
        # check
        y = ts.get()
        self.assertEqual(0, len(y))

    def test_save_unsupported_method(self):
        """
        appends new values only, this will generate error if some period are overwritten
        :return:
        """
        ts = self.coll.create(name="xyz", freq="Q", dtype=DType.int64)

        pts_time = pd.period_range('1950-01', periods=2, freq='Q')
        val = range(0, 2)
        x = pd.Series(val, index=pts_time)
        with self.assertRaises(ValueError):
            ts.save(x, method="blabla")

    def test_get_pandas(self):
        ts = self.coll.create("xyz", "Q", DType.int64)

        pts_time = pd.period_range('1950-01', periods=5, freq='Q')
        val = range(0, 5)
        x = pd.Series(val, index=pts_time)
        ts.save(x)

        xx = ts.get()
        self.assertTrue(x.equals(xx))

        time.sleep(0.01)

        pts_time2 = pd.period_range('1950-06', periods=5, freq='Q')
        val2 = range(0, 5)
        y = pd.Series(val2, index=pts_time2)
        ts.save(y)

        # then
        # retrieve most recent
        yy = ts.get()
        pts_time = pd.period_range('1950-01', periods=6, freq='Q')
        val = [0] + list(range(0, 5))
        xy = pd.Series(val, index=pts_time)
        print(pd.DataFrame({'y': y, 'x': x, 'yy': yy, 'xy': xy}))
        self.assertTrue(yy.equals(yy))

    def test_vintages(self):
        # create a first vintage by writing data
        ts = self.create_ts("xyz", freq="Q", dtype=DType.int64)

        pts_time = pd.period_range('1950-01', periods=5, freq='Q')
        val = range(0, 5)
        x = pd.Series(val, index=pts_time)
        ts.save(x)

        self.assertEqual(1, len(ts.vintages()))
        vx = ts.vintages()[0]
        print(vx)

        time.sleep(0.01)

        # save again for the next vintage
        pts_time2 = pd.period_range('1950-06', periods=5, freq='Q')
        val2 = range(0, 5)
        y = pd.Series(val2, index=pts_time2)
        ts.save(y)

        self.assertEqual(2, len(ts.vintages()))
        vy = ts.vintages()[1]
        print(vy)

    def test_get_by_vintage(self):

        # setup
        ts = self.coll.create("xyz", "Q", DType.int64)

        pts_time = pd.period_range('1950-01', periods=5, freq='Q')
        val = range(0, 5)
        x = pd.Series(val, index=pts_time)
        vx = ts.save(x)

        self.assertEqual(1, len(ts.vintages()))

        time.sleep(0.01)

        # save againg for the next vintage
        pts_time2 = pd.period_range('1950-06', periods=5, freq='Q')
        val2 = range(0, 5)
        y = pd.Series(val2, index=pts_time2)
        vy = ts.save(y, method='overwrite')

        self.assertEqual(2, len(ts.vintages()))
        # vy = ts.vintages()[1]

        # retrieve former
        xx = ts.get(vintage=vx)
        self.assertTrue(x.equals(xx))

        # retrieve latter
        yy = ts.get()
        self.assertTrue(y.equals(yy))

    def test_collection_save_single_series(self):
        """ save multiple of time series """
        raise NotImplementedError()

    def test_collection_save_list_series(self):
        """ save multiple of time series """
        raise NotImplementedError()

    def test_collection_save_dataframe(self):
        """ save multiple of time series """
        n = 5
        time = pd.period_range('1950-01', periods=5, freq='Q')
        df = pd.DataFrame({'x': pd.Series([random.randint(0, 100) for x in range(0, n)], index=time),
                           'y': pd.Series(random.randint(0, n), index=time)
                           })

        with self.assertRaises(ValueError):
            self.coll.save(df)

        tsx = self.coll.create("x", Freq.Quarterly, DType.int64)
        with self.assertRaises(ValueError) as e:
            self.coll.save(df)
        self.assertIn("x", str(e))

        tsy = self.coll.create("y", Freq.Quarterly, DType.int64)
        self.coll.save(df)

        # df2 = self.coll.get(['x', 'y'])  # list
        df2 = self.coll.to_dataframe(['x', 'y'])
        self.assertTrue(df.equals(df2))

    def test_save_dtype_validation___error(self):
        # given
        N = 5
        ts = self.coll.create("xyz", Freq.Quarterly, DType.int64)
        pts_time = pd.period_range('1950-01', periods=N, freq='Q')
        val = np.random.randn(N)
        x = pd.Series(val, index=pts_time)
        # when
        with self.assertRaises(ValueError) as e:
            x = ts.save(x)

        self.assertTrue(str(e.exception).startswith("invalid data type"))

    def test_save_itype_validation___error(self):
        # given
        N = 5
        ts = self.coll.create("xyz", Freq.Quarterly, DType.float64, itype=IType.integer)
        pts_time = pd.period_range('1950-01', periods=N, freq='Q')
        val = np.random.randn(N)
        x = pd.Series(val, index=pts_time)
        # when
        with self.assertRaises(ValueError) as e:
            x = ts.save(x)

        self.assertTrue(str(e.exception).startswith("invalid index type"))

    def test_save_freq_validation___error(self):
        # given
        N = 5
        ts = self.coll.create("xyz", Freq.Quarterly, DType.float64)
        pts_time = pd.period_range('1950-01', periods=N, freq='M')
        val = np.random.randn(N)
        x = pd.Series(val, index=pts_time)
        # when
        with self.assertRaises(ValueError) as e:
            x = ts.save(x)

        self.assertTrue(str(e.exception).startswith("invalid frequency"))


class TimeSeriesDTypeTest(unittest.TestCase):
    """ Test all data types """

    def setUp(self):

        self.space_name = "test_space"
        self.coll_name = "test_collection"

        self.chronos = pychronos.init(username="testuser", password="Testpass1!", host=HOST, port=PORT)
        if self.space_name in self.chronos.list_spaces():
            self.space = self.chronos[self.space_name]
            self.space.delete()

        self.space = self.chronos.create(self.space_name)

        if self.coll_name in self.space.list_collections():
            coll = self.space[self.coll_name]
            coll.delete()

        self.coll = self.space.create(self.coll_name)

    def tearDown(self):
        try:
            self.space = self.chronos[self.space_name]
            self.space.delete()
        except:
            pass

    def create_ts(self, name, freq="Q", dtype="int", **kwargs):

        if name in self.coll.list_timeseries():
            self.coll[name].delete()

        return self.coll.create(name, freq=freq, dtype=dtype, **kwargs)

    def test_categorical(self):
        N = 5

        pts_time = pd.period_range('1950-01', periods=N, freq='Q')
        val = pd.Categorical(['a', 'b', 'c', 'a', 'a'], ordered=False, categories=['c', 'b', 'a'])
        print(val)
        x = pd.Series(val, index=pts_time)

        ts = self.create_ts("xyz", Freq.Quarterly, DType.categorical)
        self.coll.save(x, "xyz")

        self.assertEqual("category", x.dtype.name)

        vx = ts.save(x)

        # check
        xx = ts.get()
        self.assertEqual("category", x.dtype.name)
        self.assertTrue(x.equals(xx))

    def test_categorical_with_nan(self):
        N = 5

        pts_time = pd.period_range('1950-01', periods=N, freq='Q')
        val = pd.Categorical(['a', 'b', 'c', 'a', 'd'], ordered=False, categories=['c', 'b', 'a'])
        print(val)
        x = pd.Series(val, index=pts_time)

        ts = self.create_ts("xyz", Freq.Quarterly, DType.categorical)
        self.coll.save(x, "xyz")

        self.assertEqual("category", x.dtype.name)

        vx = ts.save(x)

        # check
        xx = ts.get()
        self.assertEqual("category", x.dtype.name)
        self.assertTrue(x.equals(xx))

    def test_categorical_ordered_with_nan(self):
        N = 5

        pts_time = pd.period_range('1950-01', periods=N, freq='Q')
        val = pd.Categorical(['a', 'b', 'c', 'a', 'd'], ordered=True, categories=['c', 'b', 'a'])
        print(val)
        x = pd.Series(val, index=pts_time)

        ts = self.create_ts("xyz", Freq.Quarterly, DType.categorical, dparams={'ordered': True})
        self.coll.save(x, "xyz")

        self.assertEqual("category", x.dtype.name)

        vx = ts.save(x)

        # check
        xx = ts.get()
        self.assertEqual("category", x.dtype.name)
        self.assertTrue(x.equals(xx))

    def test_categorical_ordered_with_predefined_categories_and_nan(self):
        N = 5

        pts_time = pd.period_range('1950-01', periods=N, freq='Q')
        val = pd.Categorical(['a', 'b', 'c', 'a', 'd'], ordered=True, categories=['c', 'b', 'a'])
        print(val)
        x = pd.Series(val, index=pts_time)

        ts = self.create_ts("xyz", Freq.Quarterly, DType.categorical, dparams={'ordered': True,
                                                                               'categories': list(val.categories)
                                                                               })
        self.coll.save(x, "xyz")

        self.assertEqual("category", x.dtype.name)

        vx = ts.save(x)

        # check
        xx = ts.get()
        self.assertEqual("category", x.dtype.name)
        self.assertTrue(x.equals(xx))

    def test_integer(self):
        N = 5
        ts = self.coll.create("xyz", "Q", "int")

        pts_time = pd.period_range('1950-01', periods=N, freq='Q')
        val = pd.array([np.random.randint(10) for x in range(0, N)])
        print(val)
        x = pd.Series(val, index=pts_time)

        self.assertEqual(x.dtype.name, "int64")

        vx = ts.save(x)

        # check
        xx = ts.get()
        self.assertEqual(x.dtype.name, "int64")
        self.assertTrue(x.equals(xx))

    def test_integer_with_nan(self):
        N = 5


        pts_time = pd.period_range('1950-01', periods=N, freq='Q')
        val = pd.array([np.NaN] + [np.random.randint(10) for x in range(0, N - 1)], dtype=pd.Int64Dtype())

        x = pd.Series(val, index=pts_time)

        self.assertEqual(x.dtype.name, "Int64")

        ts = self.create_ts("xyz", Freq.Quarterly, DType.int64)
        vx = ts.save(x)

        # check
        xx = ts.get()
        self.assertEqual(x.dtype.name, "Int64")
        self.assertTrue(x.equals(xx))

    def test_bool(self):
        N = 5
        ts = self.coll.create("xyz", "Q", "bool")

        pts_time = pd.period_range('1950-01', periods=N, freq='Q')
        val = np.random.randn(N) > 0

        x = pd.Series(val, index=pts_time)

        # because one observation is None, dtype of Pandas area is object instead of "bool"
        self.assertEqual(x.dtype.name, "bool")

        vx = ts.save(x)

        # check
        xx = ts.get()
        self.assertEqual(x.dtype.name, "bool")
        self.assertTrue(x.equals(xx))

    def test_bool_with_None(self):
        N = 5
        ts = self.create_ts("xyz", Freq.Quarterly, DType.bool)

        pts_time = pd.period_range('1950-01', periods=N, freq='Q')
        val = np.append(np.random.randn(N - 1) > 0, None)

        x = pd.Series(val, index=pts_time)

        # because one observation is None, dtype of Pandas area is object instead of "bool"
        self.assertEqual(x.dtype.name, "object")

        vx = ts.save(x)

        # check
        xx = ts.get()
        self.assertEqual(x.dtype.name, "object")
        self.assertTrue(x.equals(xx))

    def garbage_test_bool(self):
        N = 5
        ts = self.coll.create("xyz", "Q", "bool")

        pts_time = pd.period_range('1950-01', periods=N, freq='Q')
        val = np.append(np.random.randn(N - 1) > 0, np.nan)
        val = np.append(np.random.randn(N - 1) > 0, np.NaN)

        x_float64 = pd.Series(np.append(np.random.randn(N - 1) > 0, np.nan))
        x_object = pd.Series(np.append(np.random.randn(N - 1) > 0, None))
        any(x_float64.isna())
        any(x_object.isna())
        x_object.dropna().dtype # still object
        pd.Series(x_object.dropna().tolist()) # now it is bool
        x_object.dropna().dtypes

        type(np.nan), type(float('nan'))

        id(np.NAN) == id(np.nan) == id(np.NaN)
        np.NAN is np.nan
        float('nan') is not float('nan')
        id(float('nan')) != id(float('nan'))

        None is None
        id(None) == id(None)

        float('none') != None

        x = np.append(np.random.randn(N - 1) > 0, np.nan)
        print(set([type(x) for x in x]))

        x = np.append(np.random.randn(N - 1) > 0, None)
        x.dtype
        set([type(x) for x in x])
        [x for x in set([type(x) for x in x]) if x is not type(None)]
        set([type(x) for x in data]) == set([type(np.bool), type(None)])

        # https://uwekorn.com/2019/09/02/boolean-array-with-missings.html
        # https://towardsdatascience.com/navigating-the-hell-of-nans-in-python-71b12558895b


        # In [1]: df = pd.DataFrame(np.random.randn(5, 3), index=['a', 'c', 'e', 'f', 'h'],
        #    ...:                   columns=['one', 'two', 'three'])
        #    ...:
        #
        # In [2]: df['four'] = 'bar'
        #
        # In [3]: df['five'] = df['one'] > 0
        #
        # In [4]: df
        # Out[4]:
        #         one       two     three four   five
        # a  0.469112 -0.282863 -1.509059  bar   True
        # c -1.135632  1.212112 -0.173215  bar  False
        # e  0.119209 -1.044236 -0.861849  bar   True
        # f -2.104569 -0.494929  1.071804  bar  False
        # h  0.721555 -0.706771 -1.039575  bar   True
        #
        # In [5]: df2 = df.reindex(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
        # In [6]: df2
        # Out[6]:
        #         one       two     three four   five
        # a  0.469112 -0.282863 -1.509059  bar   True
        # b       NaN       NaN       NaN  NaN    NaN
        # c -1.135632  1.212112 -0.173215  bar  False
        # d       NaN       NaN       NaN  NaN    NaN
        # e  0.119209 -1.044236 -0.861849  bar   True
        # f -2.104569 -0.494929  1.071804  bar  False
        # g       NaN       NaN       NaN  NaN    NaN
        # h  0.721555 -0.706771 -1.039575  bar   True
        # df = pd.DataFrame(np.random.randn(5, 3), index=['a', 'c', 'e', 'f', 'h'], columns=['one', 'two', 'three'])
        # df['four'] = 'bar'
        # df['five'] = df['one'] > 0
        # df2 = df.reindex(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
        # df2['four'].dtype # object
        # df2['four'].notna().dtype # bool
        # df2['four'].dropna().dtype # object
        # set([type(x) for x in df2['four'].dropna()]) # str
        #
        # df2['five'].dtype # object
        # df2['five'].notna().dtype # bool
        # df2['five'].dropna().dtype # object
        # set([type(x) for x in df2['five'].dropna()])  # bool
        #
        # pd.Series([1, 2, np.nan, 4], dtype=pd.Int64Dtype())
        # pd.Series([1, 2, np.nan, 4], dtype='Int64')
        # pd.Series([1, 2, 4])

        x = pd.Series(val, index=pts_time)

        # because one observation is None, dtype of Pandas area is object instead of "bool"
        self.assertEqual(x.dtype.name, "object")

        vx = ts.save(x)

        # check
        xx = ts.get()
        self.assertEqual(x.dtype.name, "object")
        self.assertTrue(x.equals(xx))

        # bool series with None is coerced to object
        # bool series with np.nan is coerced to float64
        # bool series with np.NaT is coerced to float64

    def test_float(self):
        N = 5
        ts = self.coll.create("xyz", "Q", DType.float64)

        pts_time = pd.period_range('1950-01', periods=N, freq='Q')
        val = np.random.randn(N)

        x = pd.Series(val, index=pts_time)

        self.assertEqual(x.dtype.name, "float64")

        vx = ts.save(x)

        # check
        xx = ts.get()
        self.assertEqual(x.dtype.name, "float64")
        self.assertTrue(x.equals(xx))

    def test_float_with_nan(self):
        N = 5
        ts = self.coll.create("xyz", "Q", "float")

        pts_time = pd.period_range('1950-01', periods=N, freq='Q')
        val = np.append(np.random.randn(N - 1), np.NaN)

        x = pd.Series(val, index=pts_time)

        self.assertEqual(x.dtype.name, "float64")

        vx = ts.save(x)

        # check
        xx = ts.get()
        self.assertEqual(x.dtype.name, "float64")
        self.assertTrue(x.equals(xx))


class TimeSeriesITypeTest(unittest.TestCase):
    """ Test all index types """

    def setUp(self):

        self.space_name = "test_space"
        self.coll_name = "test_collection"

        self.chronos = pychronos.init(username="testuser", password="Testpass1!", host=HOST, port=PORT)
        if self.space_name in self.chronos.list_spaces():
            self.space = self.chronos[self.space_name]
            self.space.delete()

        self.space = self.chronos.create(self.space_name)

        if self.coll_name in self.space.list_collections():
            coll = self.space[self.coll_name]
            coll.delete()

        self.coll = self.space.create(self.coll_name)

    def tearDown(self):
        try:
            self.space = self.chronos[self.space_name]
            self.space.delete()
        except:
            pass

    def create_ts(self, name, freq="Q", dtype="int", **kwargs):

        if name in self.coll.list_timeseries():
            self.coll[name].delete()

        return self.coll.create(name, freq=freq, dtype=dtype, **kwargs)

    def test_period(self):
        pass

    def test_period_frequencies(self):
        pass

    def test_timestamp(self):
        pass

    def test_relative(self):
        pass

    def test_integer(self):
        pass
