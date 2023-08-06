import numpy as np
import pandas as pd
import unittest
import pychronos
import pychronos.init
import pychronos.vintage
from pychronos import IType, DType, Freq


class VintagenTest(unittest.TestCase):

    def setUp(self):

        self.space_name = "test_space"
        self.coll_name = "test_collection"
        # HOST = 'https://tshub-dev.appspot.com'
        # PORT = 443
        HOST = "http://localhost"
        PORT = 9090

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

    def create_ts(self, name, freq="Q", dtype="int64", **kwargs):

        if name in self.coll.list_timeseries():
            self.coll[name].delete()

        return self.coll.create(name, freq=freq, dtype=dtype, **kwargs)

    def test_create_class___ok(self):
        name = "abcde12345"
        description = "my description"
        metadata = {'a': 123, 'sd': {'a': 1}}

        vt = pychronos.vintage.Vintage(name=name, description=description, metadata=metadata)

        self.assertEqual(name, vt.name)
        self.assertEqual(description, vt.description)
        self.assertEqual(metadata, vt.metadata)

        # self.assertIsNone(vt.realtime, vt.vid, vt.)

    def test_save_series_with_vintage(self):
        # given
        N = 5
        ts = self.coll.create("xyz", Freq.Quarterly, DType.float64)
        pts_time = pd.period_range('1950-01', periods=N, freq='Q')
        val = np.random.randn(N)
        val2 = np.random.randn(N)
        # https://uwekorn.com/2019/09/02/boolean-array-with-missings.html
        x = pd.Series(val, index=pts_time)
        y = pd.Series(val2, index=pts_time)

        v_name = "blabla"
        v_description = "my description"
        v_metadata = {"a": 1, "b": [1, 2], "c": {"x": 1, "y": 2}}
        vt = pychronos.Vintage(name=v_name, description=v_description, metadata=v_metadata)

        vx = ts.save(x, vintage=vt)
        vy = ts.save(y)

        # self.assertEqual(v_name, vx.name)
        self.assertEqual(ts.__coll_id__, vx.__coll_id__)
        self.assertEqual(v_name, vx.name)
        self.assertEqual(v_description, vx.description)
        self.assertEqual(v_metadata, vx.metadata)  # this is summary

        yy = ts.get()
        xx = ts.get(vx)

        self.assertTrue(xx.equals(x))
        self.assertTrue(yy.equals(y))

    def test_update(self):
        # given
        name = "abcde12345"
        description = "my description"
        metadata = {'a': 123, 'sd': {'a': 1}}

        new_name = "xyz123456"
        new_description = "anotehr description"
        new_metadata = {'b': 321, 'sd': ['a', 1]}

        N = 5
        ts = self.coll.create("xyz", Freq.Quarterly, DType.float64)
        pts_time = pd.period_range('1950-01', periods=N, freq='Q')
        val = np.random.randn(N)
        x = pd.Series(val, index=pts_time)

        v_name = "blabla"
        v_description = "my description"
        v_metadata = {"a": 1, "b": [1, 2], "c": {"x": 1, "y": 2}}
        vt = pychronos.Vintage(name=v_name, description=v_description, metadata=v_metadata)
        vx = ts.save(x, vintage=vt)

        vl = ts.vintages()
        self.assertEqual(1, len(vl))
        v = vl[0]
        self.assertEqual(v_name, v.name)
        self.assertEqual(v_description, v.description)
        self.assertEqual(v_metadata, v.metadata)

    def test_update___name_already_exists_error(self):
        N = 5
        ts = self.coll.create("xyz", Freq.Quarterly, DType.float64)
        pts_time = pd.period_range('1950-01', periods=N, freq='Q')
        val = np.random.randn(N)
        x = pd.Series(val, index=pts_time)

        v_name = "blabla"
        v_description = "my description"
        v_metadata = {"a": 1, "b": [1, 2], "c": {"x": 1, "y": 2}}
        vt = pychronos.Vintage(name=v_name, description=v_description, metadata=v_metadata)
        vx = ts.save(x, vintage=vt)

        ts2 = self.coll.create("xyz2", Freq.Quarterly, DType.float64)
        pts_time2 = pd.period_range('1970-01', periods=N, freq='Q')
        val2 = np.random.randn(N)
        x2 = pd.Series(val2, index=pts_time2)

        # try saving with the same vintage name
        with self.assertRaises(ValueError) as e:
            vx2 = ts2.save(x2, vintage=vt)

        print(e)

    def test_history(self):
        pass



if False:
    import pychronos
    chronos = pychronos.init(username='admin', password='Admin1!')
    chronos.list_spaces()
    sd = chronos['sample_data']
