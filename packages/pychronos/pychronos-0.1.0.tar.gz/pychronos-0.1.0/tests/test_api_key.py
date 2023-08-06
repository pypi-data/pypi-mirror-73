import unittest
import pychronos
from pychronos import Chronos

username="testuser"
password="Testpass1!"
host = "http://localhost"
port = 9090


class InitTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.chronos = pychronos.init(username=username, password=password,
                                     host="http://localhost", port=9090,
                                     base_path='/api')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_init___ok(self):

        x = pychronos.init(username=username, password=password, host=host, port=port)
        self.assertIsInstance(x, Chronos)

    def test_init___no_connection(self):

        with self.assertRaises(ConnectionError):
            pychronos.init(username=username, password=password, host="http://blabla.com", port=port)

    def test_init___wrong_port(self):

        with self.assertRaises(ConnectionError):
            pychronos.init(username=username, password=password, host="http://localhost", port=8888)

