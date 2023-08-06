import pandas as pd
import unittest

from pandas._libs.tslibs.period import IncompatibleFrequency

import pychronos
from pychronos import DType, Freq, Vintage


class CollectionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.space_name = "test_space"
        cls.coll_name = "test_collection"

        # self.chronos = pychronos.init(username="testuser", password="Testpass1!", host="https://tshub-dev.appspot.com", port=443)
        cls.chronos = pychronos.init(username="testuser", password="Testpass1!", host="http://localhost", port=9090)

    def setUp(self):

        if self.space_name in self.chronos.list_spaces():
            self.chronos[self.space_name].delete()

        self.space = self.chronos.create(self.space_name)
        self.collection = self.space.create(self.coll_name)

    def tearDown(self):
        self.space.delete()

    def test_create(self):
        name = "abcde12345"
        title = "my title"
        description = "my description"

        if name in self.space.list_collections():
            self.space[name].delete()

        self.space.create(name, title, description)
        self.assertIn(name, self.space.list_collections())

        coll = self.space[name]

        self.assertEqual(title, coll.title)
        self.assertEqual(description, coll.description)

    def test_update(self):
        name = "abcde12345"
        title = "my title"
        description = "my description"

        if name in self.space.list_collections():
            self.space[name].delete()

        self.space.create(name, title, description)
        self.assertIn(name, self.space.list_collections())

        coll = self.space[name]

        self.assertEqual(title, coll.title)
        self.assertEqual(description, coll.description)

        title_new = "new title"
        coll.title = title_new
        self.assertEqual(title_new, coll.title)

        description_new = "new description"
        coll.description = description_new
        self.assertEqual(description_new, coll.description)

        name_new = "x12345abcde"
        coll.name = name_new
        self.assertEqual(name_new, coll.name)

        cc = self.space[name_new]
        self.assertEqual(cc.__coll_id__, coll.__coll_id__)

    def test_delete___ok(self):
        # given
        name = "fdgsdfgfdg"

        self.assertNotIn(name, self.space.list_collections())

        self.space.create(name)

        self.assertIn(name, self.space.list_collections())

        self.space[name].delete()

        self.assertNotIn(name, self.space.list_collections())

    def test_delete___not_exists(self):
        # given
        name = "fdgsdfgfdg"
        self.assertNotIn(name, self.space.list_collections())

        with self.assertRaises(ValueError):
            self.space[name].delete()

    def test_get_timeseries___ok(self):
        # given
        name = "gdfads"
        ts = self.collection.create(name=name, itype="p", freq=Freq.Quarterly, dtype=DType.int64)

        # when
        ts2 = self.collection[name]

        # then
        self.assertEqual(ts, ts2)

    def test_get_timeseries___not_found(self):
        # given
        name = "gdfads"

        # when
        with self.assertRaises(ValueError):
            self.collection[name]

    def test_get_function___ok(self):
        # given
        name = "ts1"
        ts1 = self.collection.create(name=name, itype="p", freq=Freq.Quarterly, dtype=DType.int64)
        x1 = pd.Series(range(0, 5), index=pd.period_range('1950-01', periods=5, freq='Q'))
        ts1.save(x1)

        name = "ts2"
        ts2 = self.collection.create(name=name, itype="p", freq=Freq.Daily, dtype=DType.int64)
        x2 = pd.Series(range(10, 15), index=pd.period_range('2050-01-01', periods=5, freq='D'))
        ts2.save(x2)

        # when
        ts_single = self.collection.get('ts1')
        ts_single_list = self.collection.get(['ts2'])
        ts_many_list = self.collection.get(['ts1', 'ts2'])
        ts_many_tuple = self.collection.get(('ts2', 'ts1',))

        # then
        self.assertIsInstance(ts_single, pd.Series)
        self.assertTrue(x1.equals(ts_single))

        self.assertIsInstance(ts_single_list, list)
        self.assertIsInstance(ts_many_list, list)
        self.assertIsInstance(ts_many_tuple, list)
        self.assertSetEqual(set(['ts1', 'ts2']), set([x.name for x in ts_many_list]))
        self.assertSetEqual(set(['ts1', 'ts2']), set([x.name for x in ts_many_tuple]))

        self.assertTrue(x1.equals([x for x in ts_many_list if x.name == 'ts1'][0]))
        self.assertTrue(x2.equals([x for x in ts_many_list if x.name == 'ts2'][0]))

    def test_ts_dataframe___ok(self):
        # given
        name = "ts1"
        ts1 = self.collection.create(name=name, itype="p", freq=Freq.Quarterly, dtype=DType.int64)
        x1 = pd.Series(range(0, 5), index=pd.period_range('1950-01', periods=5, freq='Q'))
        ts1.save(x1)

        name = "ts2"
        ts2 = self.collection.create(name=name, itype="p", freq=Freq.Quarterly, dtype=DType.int64)
        x2 = pd.Series(range(10, 15), index=pd.period_range('2050-01-01', periods=5, freq='Q'))
        ts2.save(x2)

        # when
        ts_single = self.collection.to_dataframe('ts1')
        ts_single_list = self.collection.to_dataframe(['ts2'])
        ts_many_list = self.collection.to_dataframe(['ts1', 'ts2'])

        # then
        self.assertIsInstance(ts_single, pd.DataFrame)
        self.assertTrue(pd.DataFrame({'ts1': x1}).equals(ts_single))

        self.assertIsInstance(ts_single_list, pd.DataFrame)
        self.assertIsInstance(ts_many_list, pd.DataFrame)
        self.assertSetEqual(set(['ts1', 'ts2']), set(ts_many_list.columns))

    def test_ts_dataframe___IncompatibleFrequency(self):
        # given
        name = "ts1"
        ts1 = self.collection.create(name=name, itype="p", freq=Freq.Quarterly, dtype=DType.int64)
        x1 = pd.Series(range(0, 5), index=pd.period_range('1950-01', periods=5, freq='Q'))
        ts1.save(x1)

        name = "ts2"
        ts2 = self.collection.create(name=name, itype="p", freq=Freq.Daily, dtype=DType.int64)
        x2 = pd.Series(range(10, 15), index=pd.period_range('2050-01-01', periods=5, freq='D'))
        ts2.save(x2)

        # when
        with self.assertRaises(IncompatibleFrequency):
            self.collection.to_dataframe(['ts1', 'ts2'])

    def test_get_function_not_found___error(self):

        with self.assertRaises(ValueError) as e:
            ts_single = self.collection.get('ts1')

        with self.assertRaises(ValueError) as e:
            ts_single_list = self.collection.get(['ts2'])

        with self.assertRaises(ValueError) as e:
            ts_many_list = self.collection.get(['ts1', 'ts2'])

    def test_get_by_vintage(self):
        raise NotImplementedError()

    def test_save_single_series(self):
        data = pd.Series(range(0, 5), index=pd.period_range('1950-01', periods=5, freq='Q'), name="x1")
        self.collection.save(data, name="x1")

    def test_save_single_series_no_name___error(self):
        x1 = pd.Series(range(0, 5), index=pd.period_range('1950-01', periods=5, freq='Q'))
        self.collection.save(x1, name="x1")

    def test_save_single_series_no_name___ok(self):
        x1 = pd.Series(range(0, 5), index=pd.period_range('1950-01', periods=5, freq='Q'))
        self.collection.save(x1, name="x1")

    def test_save_list_of_series(self):
        x1 = pd.Series(range(0, 5), index=pd.period_range('1950-01', periods=5, freq='Q'), name="x1")
        x2 = pd.Series(range(0, 5), index=pd.period_range('1950-01', periods=5, freq='Q'), name="x2")

        ts1 = self.collection.create(name='x1', itype="p", freq=Freq.Quarterly, dtype=DType.int64)
        ts2 = self.collection.create(name='x2', itype="p", freq=Freq.Quarterly, dtype=DType.int64)

        data = [x1, x2]
        self.collection.save(data)

    def test_save_list_of_series_names(self):
        x1 = pd.Series(range(0, 5), index=pd.period_range('1950-01', periods=5, freq='Q'))
        x2 = pd.Series(range(0, 5), index=pd.period_range('1950-01', periods=5, freq='Q'))

        ts1 = self.collection.create(name='x1', itype="p", freq=Freq.Quarterly, dtype=DType.int64)
        ts2 = self.collection.create(name='x2', itype="p", freq=Freq.Quarterly, dtype=DType.int64)

        data = [x1, x2]
        self.collection.save(data, names=['x1', 'x2'])

    def test_save_dataframe___ok(self):
        x1 = pd.Series(range(0, 5), index=pd.period_range('1950-01', periods=5, freq='Q'), name="x1")
        x2 = pd.Series(range(10, 15), index=pd.period_range('1950-01', periods=5, freq='Q'), name="x2")

        ts1 = self.collection.create(name='x1', itype="p", freq=Freq.Quarterly, dtype=DType.int64)
        ts2 = self.collection.create(name='x2', itype="p", freq=Freq.Quarterly, dtype=DType.int64)

        data = pd.concat([x1, x2], axis=1)
        self.collection.save(data)

        xx1 = ts1.get()
        xx2 = ts2.get()

        self.assertTrue(x1.equals(xx1))
        self.assertTrue(x2.equals(xx2))

    # def test_save_dataframe___no_name_errror(self):
    #     x1 = pd.Series(range(0, 5), index=pd.period_range('1950-01', periods=5, freq='Q'), name="x1")
    #     x2 = pd.Series(range(0, 5), index=pd.period_range('1950-01', periods=5, freq='Q')) # no name
    #     data = pd.concat([x1, x2], axis=1)
    #
    #     ts1 = self.collection.create(name='x1', itype="p", freq=Freq.Quarterly, dtype=DType.int64)
    #     ts2 = self.collection.create(name='x2', itype="p", freq=Freq.Quarterly, dtype=DType.int64)
    #
    #     self.collection.save(data)

    def test_save_dataframe_with_names___ok(self):
        x1 = pd.Series(range(0, 5), index=pd.period_range('1950-01', periods=5, freq='Q'), name='z1')
        x2 = pd.Series(range(0, 5), index=pd.period_range('1950-01', periods=5, freq='Q'), name='z2')
        data = pd.concat([x1, x2], axis=1)

        ts1 = self.collection.create(name='x1', itype="p", freq=Freq.Quarterly, dtype=DType.int64)
        ts2 = self.collection.create(name='x2', itype="p", freq=Freq.Quarterly, dtype=DType.int64)

        x2 = pd.Series(range(0, 5), index=pd.period_range('1950-01', periods=5, freq='Q'))  # no name

        self.collection.save(data, names=['x1', 'x2'])

        xx1 = ts1.get()
        xx2 = ts2.get()

        self.assertTrue(x1.equals(xx1))
        self.assertTrue(x2.equals(xx2))

    def test_save_dataframe_with_vintage___ok(self):
        vname = "myvintage"
        vdesc = 'my description'
        vmetadata = {'param1': 123, 'param2': 456}

        x1 = pd.Series(range(0, 5), index=pd.period_range('1950-01', periods=5, freq='Q'), name='z1')
        x2 = pd.Series(range(0, 5), index=pd.period_range('1950-01', periods=5, freq='Q'), name='z2')
        data = pd.concat([x1, x2], axis=1)

        ts1 = self.collection.create(name='x1', itype="p", freq=Freq.Quarterly, dtype=DType.int64)
        ts2 = self.collection.create(name='x2', itype="p", freq=Freq.Quarterly, dtype=DType.int64)

        x2 = pd.Series(range(0, 5), index=pd.period_range('1950-01', periods=5, freq='Q'))  # no name

        self.collection.save(data,
                             names=['x1', 'x2'],
                             vintage=Vintage(name=vname, description=vdesc, metadata=vmetadata))

        vintages = self.collection.vintages()
        self.assertIn(vname, [v.name for v in vintages])
        v = [v for v in vintages if v.name == vname][0]
        self.assertEqual(vmetadata, v.metadata)
        self.assertEqual(vdesc, v.description)

    def test_vintages___ok(self):
        pass

    def test_history(self):
        name = "abcde12345"
        title = "my title"
        description = "my description"

        if name in self.space.list_collections():
            self.space[name].delete()

        self.space.create(name, title, description)
        self.assertIn(name, self.space.list_collections())

        coll = self.space[name]

        self.assertEqual(title, coll.title)
        self.assertEqual(description, coll.description)

        title_new = "new title"
        coll.title = title_new
        self.assertEqual(title_new, coll.title)

        description_new = "new description"
        coll.description = description_new
        self.assertEqual(description_new, coll.description)

        name_new = "x12345abcde"
        coll.name = name_new
        self.assertEqual(name_new, coll.name)

        cc = self.space[name_new]
        self.assertEqual(cc.__coll_id__, coll.__coll_id__)

        hist = cc.history()

        self.assertEqual(4, len(hist))

        # first element is current
        self.assertEqual(cc.__real_start__, hist[0].__real_start__)
        self.assertEqual(cc.__real_end__, hist[0].__real_end__)

        with self.assertRaises(TypeError):
            hist[1].title = "test test"
        with self.assertRaises(TypeError):
            hist[1].name = "test test"
        with self.assertRaises(TypeError):
            hist[1].description = "test test"
        with self.assertRaises(TypeError):
            hist[1].delete()
        with self.assertRaises(TypeError):
            hist[1].list_timeseries()
        with self.assertRaises(TypeError):
            hist[1]['test test']
        with self.assertRaises(TypeError):
            hist[1].get('test test')
        with self.assertRaises(TypeError):
            hist[1].to_dataframe('test test')
        with self.assertRaises(TypeError):
            hist[1].create('test test')
        with self.assertRaises(TypeError):
            hist[1].save('test test')
        with self.assertRaises(TypeError):
            hist[1].vintages()
        with self.assertRaises(TypeError):
            hist[1].history('test test')



# import pychronos
# chronos = pychronos.init(username="testuser", password="Testpass1!", host="https://tshub-dev.appspot.com", port=443)
# chronos.list_space_names()
# chronos.create("blabla", "dsafdsf dsfads", "dfa dsf dsfdsf sdafdsfads fdsafdsa")
# s = chronos['mytestspace']
# s.info()
