import unittest
import pychronos
from pychronos import Collection


class SpaceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.space_name = "test_space"
        # self.chronos = pychronos.init(username="testuser", password="Testpass1!", host="https://tshub-dev.appspot.com", port=443)
        cls.chronos = pychronos.init(username="testuser", password="Testpass1!", host="http://localhost", port=9090)

    def setUp(self):

        if self.space_name in self.chronos.list_spaces():
            self.chronos[self.space_name].delete()

        self.space = self.chronos.create(self.space_name)

    def tearDown(self):
        try:
            self.chronos[self.space_name].delete()
        except:
            pass

    def test_create_space(self):
        name = "abcde12345"
        title = "my space title"
        description = "my description"

        if name in self.chronos.list_spaces():
            self.chronos[name].delete()

        self.chronos.create(name, title, description)
        self.assertIn(name, self.chronos.list_spaces())

        s = self.chronos[name]

        self.assertEqual(title, s.title)
        self.assertEqual(description, s.description)

    def test_get_collection___not_exists(self):
        # given
        name = "fdgsdfgfdg"
        self.assertNotIn(name, self.space.list_collections())

        with self.assertRaises(ValueError):
            self.space[name]

    def test_get_collection___ok(self):
        # given
        name = "fdgsdfgfdg"
        self.assertNotIn(name, self.space.list_collections())

        # when
        self.space.create(name)

        # then

        coll = self.space[name]

        self.assertIsInstance(coll, Collection)
        self.assertEqual(name, coll.name)

    def test_update(self):
        name = "abcde12345"
        name_new = "x12345abcde"
        title = "my space title"
        description = "my description"

        if name in self.chronos.list_spaces():
            self.chronos[name].delete()
        if name_new in self.chronos.list_spaces():
            self.chronos[name_new].delete()

        self.chronos.create(name, title, description)
        self.assertIn(name, self.chronos.list_spaces())

        s = self.chronos[name]

        self.assertEqual(title, s.title)
        self.assertEqual(description, s.description)

        title_new = "new title"
        s.title = title_new
        self.assertEqual(title_new, s.title)

        description_new = "new description"
        s.description = description_new
        self.assertEqual(description_new, s.description)

        s.name = name_new
        self.assertEqual(name_new, s.name)

        ss = self.chronos[name_new]
        self.assertEqual(ss.__space_id__, s.__space_id__)

    def test_delete(self):

        self.assertIn(self.space_name, self.chronos.list_spaces())

        self.chronos[self.space_name].delete()

        self.assertNotIn(self.space_name, self.chronos.list_spaces())

    def test_history(self):
        name = "df234rwea"
        new_name = "fnkjdsnfkj"
        title = "my title"
        description = "my description"

        # cleanup
        if name in self.chronos.list_spaces():
            self.chronos[name].delete()
        if new_name in self.chronos.list_spaces():
            self.chronos[new_name].delete()


        self.chronos.create(name, title, description)
        self.assertIn(name, self.chronos.list_spaces())

        s = self.chronos[name]

        self.assertEqual(title, s.title)
        self.assertEqual(description, s.description)

        title_new = "new title"
        s.title = title_new
        self.assertEqual(title_new, s.title)

        description_new = "new description"
        s.description = description_new
        self.assertEqual(description_new, s.description)

        name_new = new_name
        s.name = name_new
        self.assertEqual(name_new, s.name)

        ss = self.chronos[name_new]
        self.assertEqual(ss.__space_id__, s.__space_id__)

        hist = ss.history()

        self.assertEqual(4, len(hist))

        # first element is current
        self.assertEqual(ss.__real_start__, hist[0].__real_start__)
        self.assertEqual(ss.__real_end__, hist[0].__real_end__)

        with self.assertRaises(TypeError):
            hist[1].title = "test test"
        with self.assertRaises(TypeError):
            hist[1].name = "test test"
        with self.assertRaises(TypeError):
            hist[1].description = "test test"
        with self.assertRaises(TypeError):
            hist[1].delete()
        with self.assertRaises(TypeError):
            hist[1]['test_test']
        with self.assertRaises(TypeError):
            hist[1].create('test test')
        with self.assertRaises(TypeError):
            hist[1].history('test test')
