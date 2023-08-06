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

    def test_all(self):
        pass