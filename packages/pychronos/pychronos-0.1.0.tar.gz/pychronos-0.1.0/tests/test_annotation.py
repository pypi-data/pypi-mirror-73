import numpy as np
import pandas as pd
import unittest

from pandas._libs.tslibs.period import IncompatibleFrequency

import pychronos
from pychronos import DType, Freq, Vintage
from tests.fixtures import fake

HOST = "http://localhost"
PORT = 9090


class AnnotationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.space_name = fake.obj_name()
        cls.coll_name = "test_collection"

        # self.chronos = pychronos.init(username="testuser", password="Testpass1!", host="https://tshub-dev.appspot.com", port=443)
        cls.chronos = pychronos.init(username="testuser", password="Testpass1!", host="http://localhost", port=9090)

    def setUp(self):

        self.space_name = fake.obj_name()
        self.coll_name = fake.obj_name()

        self.chronos = pychronos.init(username="testuser", password="Testpass1!", host=HOST, port=PORT)

        if self.space_name in self.chronos.list_spaces():
            self.space = self.chronos[self.space_name]
            self.space.delete()

        self.space = self.chronos.create(self.space_name)

        if self.coll_name in self.space.list_collections():
            coll = self.space[self.coll_name]
            coll.delete()

        self.coll = self.space.create(self.coll_name)

        N = 5
        self.ts_name = fake.obj_name()
        self.ts = self.coll.create(self.ts_name, Freq.Quarterly, DType.float64)
        pts_time = pd.period_range('1950-01', periods=N, freq='Q')
        val = np.random.randn(N)
        x = pd.Series(val, index=pts_time)

        vx = self.ts.save(x)

    def tearDown(self):
        self.space.delete()

    def test_create_annotation_via_collection(self):
        text = fake.obj_name()
        text_format = "txt"
        attributes = {'a': 1234, 'b': "dsfdsafds"}

        a = self.coll.annotate(text=text, text_format=text_format, attributes=attributes)

        annots = self.coll.annotations()
        ts_annots = self.ts.annotations()

        self.assertIn(a.aid, [x.aid for x in annots])

        aa = [x for x in annots if x.aid == a.aid][0]
        self.assertEqual(text, aa.text)
        self.assertEqual(text_format, aa.format)
        self.assertEqual(attributes, aa.attributes)

    def test_create_annotation_via_timeseries(self):
        text = fake.obj_name()
        textformat = "txt"
        attributes = {'a': 1234, 'b': "dsfdsafds"}
        index = self.ts.get().index[3]
        a = self.ts.annotate(text=text, text_format=textformat, index=index, attributes=attributes)

        annots = self.coll.annotations()
        ts_annots = self.ts.annotations()

        aa = [x for x in annots if x.aid == a.__aid__][0]

        # [x for x in aa if x]
        self.assertEqual(text, aa.text)
        self.assertEqual(textformat, aa.format)
        self.assertEqual(attributes, aa.attributes)

        # self.assertEqual(title, coll.title)
        # self.assertEqual(description, coll.description)

    def test_add_target_timeseries(self):
        text = fake.obj_name()
        text_format = "txt"
        a = self.coll.annotate(text=text, text_format=text_format)
        index = self.ts.get().index[3]
        tsid = self.ts
        a.annotate(timeseries=self.ts)

        # then
        ts_annots = self.ts.annotations()
        aa = ts_annots[0]
        self.assertEqual(text, aa.text)
        self.assertEqual(text_format, aa.format)
        self.assertEqual(1, len(aa.targets))
        self.assertIsNone(aa.targets[0].index)
        self.assertEqual(self.ts.tsid, aa.targets[0].timeseries.tsid)
        self.assertIsNone(aa.targets[0].real_start)

    def test_add_target_period(self):
        text = fake.obj_name()
        _format = "txt"
        a = self.coll.annotate(text=text, text_format=_format)
        index = self.ts.get().index[3]
        tsid = self.ts
        a.annotate(index=index)

        # then
        aa = self.coll.annotation(a.symbol)
        self.assertEqual(text, aa.text)
        self.assertEqual(_format, aa.format)
        self.assertEqual(1, len(aa.targets))
        self.assertEqual(index, aa.targets[0].index)
        self.assertIsNone(aa.targets[0].timeseries)
        self.assertIsNone(aa.targets[0].real_start)

    def test_add_target_observation(self):
        text = fake.obj_name()
        text_format = "txt"
        a = self.coll.annotate(text=text, text_format=text_format)
        index = self.ts.get().index[3]
        a.annotate(timeseries=self.ts, index=index)

        # then
        ts_annots = self.ts.annotations()
        aa = ts_annots[0]
        self.assertEqual(text, aa.text)
        self.assertEqual(text_format, aa.format)
        self.assertEqual(1, len(aa.targets))
        self.assertEqual(index, aa.targets[0].index)
        self.assertEqual(self.ts.tsid, aa.targets[0].timeseries.tsid)
        self.assertIsNone(aa.targets[0].real_start)

    def test_remove_target(self):
        text = fake.sentence()
        text_format = "txt"
        a = self.coll.annotate(text=text, text_format=text_format)
        index = self.ts.get().index[3]
        tsid = self.ts
        a.annotate(timeseries=self.ts, index=index)

        # then
        ts_annots = self.ts.annotations()
        aa = ts_annots[0]
        self.assertEqual(text, aa.text)
        self.assertEqual(text_format, aa.format)
        self.assertEqual(1, len(aa.targets))
        aa.targets[0].delete()

        ts_annots = self.ts.annotations()
        self.assertFalse(ts_annots)

    def test_update_text(self):
        symbol = "abcde12345"
        text = fake.sentence()
        text2 = fake.sentence()
        _format = "txt"

        a = self.coll.annotate(text=text, text_format=_format)
        a.update(text=text2)

        self.assertEqual(text2, a.text)
        aa = self.coll.annotation(a.symbol)
        self.assertEqual(text2, aa.text)

    def test_update_symbol(self):
        symbol = fake.word()
        symbol2 = fake.word()
        text = fake.sentence()
        text_format = "txt"

        a = self.coll.annotate(symbol=symbol, text=text, text_format=text_format)

        a.update(symbol=symbol2)

        self.assertEqual(symbol2, a.symbol)
        aa = self.coll.annotation(symbol2)
        self.assertEqual(symbol2, aa.symbol)
        self.assertEqual(text, aa.text)

    def test_update_symbol___exists_error(self):
        symbol = fake.word()
        symbol2 = fake.word()
        text = fake.sentence()
        text2 = fake.sentence()
        _format = "txt"

        a = self.coll.annotate(symbol=symbol, text=text, text_format=_format)
        b = self.coll.annotate(symbol=symbol2, text=text2, text_format=_format)

        with self.assertRaises(Exception):
            a.update(symbol=symbol2)
