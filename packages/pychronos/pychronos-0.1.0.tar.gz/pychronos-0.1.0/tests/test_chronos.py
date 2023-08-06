import time
import unittest
import pychronos
from pychronos import Chronos
from openapi_client.exceptions import ApiException


class ChronosTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_instance_without_init(self):
        pychronos.close()

        with self.assertRaises(RuntimeError):
            c = Chronos()

    def test_login___ok(self):
        # when
        chronos = pychronos.init(username="testuser", password="Testpass1!", host="http://localhost", port=9090, base_path='/api')
        token = pychronos._configuration.access_token

        pychronos._user_api_instance.app_api_user_ping()

        chronos.logout()

        self.assertEqual("", pychronos._configuration.access_token)

        with self.assertRaises(ApiException) as e:
            pychronos._user_api_instance.app_api_user_ping()

        self.assertEqual(401, e.exception.status)

        time.sleep(1)

        chronos.login(username="testuser", password="Testpass1!")

        self.assertEqual(len(token), len(pychronos._configuration.access_token))
        self.assertNotEqual(token, pychronos._configuration.access_token)

        pychronos._user_api_instance.app_api_user_ping()

    def test_login_different_user___ok(self):
        # when
        chronos = pychronos.init(username="testuser", password="Testpass1!", host="http://localhost", port=9090, base_path='/api')

        chronos.logout()

        with self.assertRaises(Exception) as e:
            pychronos._user_api_instance.app_api_user_ping()

        self.assertEqual(401, e.exception.status)

        chronos.login(username="testuser2", password="Testpass2!")

        print(pychronos._user_api_instance.app_api_user_ping())

    def test_close___ok(self):
        # when
        chronos = pychronos.init(username="testuser", password="Testpass1!", host="http://localhost", port=9090, base_path='/api')
