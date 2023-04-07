#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from unittest.mock import patch
import json
import os
import pep8
import unittest

DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "skip if  fs")
class TestDBStorageGet(unittest.TestCase):
    """Tests get method of the DBStorage class"""

    def setUp(self):
        """Set up for the tests"""

        self.storage = DBStorage()
        self.storage.reload()
        self.new_state = State(name="California")
        self.new_state.save()
        self.new_city = City(name="San Francisco", state_id=self.new_state.id)
        self.new_city.save()

    def tearDown(self):
        """Tear down after the tests"""

        self.storage.delete(self.new_city)
        self.storage.delete(self.new_state)
        self.storage.save()
        self.storage.close()

    def test_get_existing_object(self):
        """Test get() with an object that exists"""
        obj = self.storage.get(City, self.new_city.id)
        self.assertEqual(obj.id, self.new_city.id)

    def test_get_nonexistent_object(self):
        """Test get() with an object that does not exist"""
        obj = self.storage.get(State, "nonexistent")
        self.assertIsNone(obj)


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "skip if not db")
class TestDBStorageCount(unittest.TestCase):
    """Tests the count() method of the DBStorage class"""

    def setUp(self):
        """Set up for the tests"""

        self.storage = DBStorage()
        self.storage.reload()
        self.new_state1 = State(name="California")
        self.new_state2 = State(name="New York")
        self.new_state3 = State(name="Texas")
        self.new_state1.save()
        self.new_state2.save()
        self.new_state3.save()

    def tearDown(self):
        """Tear down after the tests"""

        self.storage.delete(self.new_state1)
        self.storage.delete(self.new_state2)
        self.storage.delete(self.new_state3)
        self.storage.save()
        self.storage.close()

    def test_count_all_objects(self):
        """Test count() with no arguments"""
        count = self.storage.count()
        self.assertEqual(count, 3)

    def test_count_some_objects(self):
        """Test count() with a class argument"""
        count = self.storage.count(State)
        self.assertEqual(count, 3)

    def test_count_nonexistent_class(self):
        """Test count() with a nonexistent class argument"""
        count = self.storage.count(Amenity)
        self.assertEqual(count, 0)


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "skip if not db")
class TestDBStorageCreateAndUpdate(unittest.TestCase):
    """Tests for creating and updating objects with DBStorage"""

    def setUp(self):
        """Set up for the tests"""
        self.storage = DBStorage()
        self.storage.reload()

    def tearDown(self):
        """Tear down after the tests"""
        self.storage.close()

    def test_create_state(self):
        """Test creating a new State object and saving it to the database"""
        new_state = State(name="Test State")
        self.storage.new(new_state)
        self.storage.save()
        retrieved_state = self.storage.get(State, new_state.id)
        self.assertIsNotNone(retrieved_state)
        self.assertEqual(retrieved_state.name, "Test State")
        self.storage.delete(new_state)
        self.storage.save()

    def test_update_state(self):
        """Test updating an existing State object and saving the
        changes to the database"""
        new_state = State(name="Test State")
        self.storage.new(new_state)
        self.storage.save()

        new_state.name = "Updated Test State"
        self.storage.save()

        retrieved_state = self.storage.get(State, new_state.id)
        self.assertIsNotNone(retrieved_state)
        self.assertEqual(retrieved_state.name, "Updated Test State")
        self.storage.delete(new_state)
        self.storage.save()

    def test_delete_nonexistent_state(self):
        """Test attempting to delete a State object that doesn't exist"""
        nonexistent_state = State(id="nonexistent_id")
        self.storage.delete(nonexistent_state)
        self.storage.save()
        self.assertIsNone(self.storage.get(State, "nonexistent_id"))

    def test_all_with_filter(self):
        """Test filtering the results of the `all` method by class"""
        new_state1 = State(name="Test State 1")
        new_state2 = State(name="Test State 2")
        new_city = City(name="Test City", state_id=new_state1.id)
        self.storage.new(new_state1)
        self.storage.new(new_state2)
        self.storage.new(new_city)
        self.storage.save()

        all_states = self.storage.all(State)
        all_cities = self.storage.all(City)

        self.assertEqual(len(all_states), 2)
        self.assertEqual(len(all_cities), 1)

        self.storage.delete(new_city)
        self.storage.delete(new_state1)
        self.storage.delete(new_state2)
        self.storage.save()

    def test_object_relationships(self):
        """Test the proper handling of object relationships"""
        new_state = State(name="Test State")
        self.storage.new(new_state)
        self.storage.save()

        new_city = City(name="Test City", state_id=new_state.id)
        self.storage.new(new_city)
        self.storage.save()

        retrieved_city = self.storage.get(City, new_city.id)
        self.assertIsNotNone(retrieved_city)
        self.assertEqual(retrieved_city.state_id, new_state.id)

        retrieved_state = self.storage.get(State, new_state.id)
        self.assertIsNotNone(retrieved_state)

        self.assertIn(new_city, retrieved_state.cities)

        self.storage.delete(new_city)
        self.storage.delete(new_state)
        self.storage.save()


@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
class TestDBStorageNewAndDelete(unittest.TestCase):
    """Test the new and delete methods of the DBStorage class"""

    def setUp(self):
        """Set up for the tests"""
        self.storage = DBStorage()
        self.storage.reload()
        self.new_state = State(name="Florida")

    def tearDown(self):
        """Tear down after the tests"""
        self.storage.close()

    def test_new_object(self):
        """Test adding a new object to the database"""
        self.storage.new(self.new_state)
        retrieved_state = self.storage.get(State, self.new_state.id)
        self.assertIsNone(retrieved_state)  # not saved yet
        self.storage.save()
        retrieved_state = self.storage.get(State, self.new_state.id)
        self.assertIsNotNone(retrieved_state)
        self.assertEqual(retrieved_state.name, "Florida")

    def test_delete_object(self):
        """Test deleting an object from the database"""
        self.storage.new(self.new_state)
        self.storage.save()
        retrieved_state = self.storage.get(State, self.new_state.id)
        self.assertIsNotNone(retrieved_state)
        self.storage.delete(self.new_state)
        self.storage.save()
        retrieved_state = self.storage.get(State, self.new_state.id)
        self.assertIsNone(retrieved_state)


# @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
# class TestDBStorageReloadAndClose(unittest.TestCase):
#     """Test the reload and close methods of the DBStorage class"""
#
#     def setUp(self):
#         """Set up for the tests"""
#         self.storage = DBStorage()
#         self.storage.reload()
#         self.new_state = State(name="Colorado")
#
#     def tearDown(self):
#         """Tear down after the tests"""
#         retrieved_state = self.storage.get(State, self.new_state.id)
#         if retrieved_state:
#             self.storage.delete(retrieved_state)
#             self.storage.save()
#         self.storage.close()
#
#     def test_reload_method(self):
#         """Test reloading data from the database"""
#         self.storage.new(self.new_state)
#         self.storage.save()
#         self.storage.close()  # Close current session
#         self.storage.reload()  # Reload data from the database
#
#         retrieved_state = self.storage.get(State, self.new_state.id)
#         self.assertIsNotNone(retrieved_state)
#         self.assertEqual(retrieved_state.name, "Colorado")
#
#     def test_close_method(self):
#         """Test closing the database session"""
#         self.storage.new(self.new_state)
#         self.storage.save()
#         self.storage.close()  # Close current session
#
#         # Attempt to query the database after closing the session
#         with self.assertRaises(Exception):
#             self.storage.all(State)


@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
class TestDBStorageSaveWithoutChanges(unittest.TestCase):
    def setUp(self):
        """Comment"""
        self.storage = DBStorage()
        self.storage.reload()

    def tearDown(self):
        """Comment"""
        self.storage.close()
        for obj in self.storage.all().values():
            self.storage.delete(obj)
        self.storage.save()

    @patch('models.engine.db_storage.DBStorage.save')
    def test_save_without_changes(self, save_mock):
        """Comment"""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        save_mock.assert_called_once()

        # Save without changes
        self.storage.save()
        save_mock.assert_called_once()


@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
class TestDBStorageEnvironmentVariables(unittest.TestCase):
    """Comment"""

    def setUp(self):
        """Comment"""
        self.storage = DBStorage()
        self.storage.reload()

    def tearDown(self):
        """Comment"""
        self.storage.close()
        for obj in self.storage.all().values():
            self.storage.delete(obj)
        self.storage.save()

    def test_missing_environment_variables(self):
        """Comment"""
        with patch.dict('os.environ',
                        {'HBNB_MYSQL_USER': '', 'HBNB_MYSQL_PWD': ''},
                        clear=True):
            with self.assertRaises(Exception):
                self.storage.__engine = None
                self.storage.reload()


@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
class TestDBStorageInvalidClassType(unittest.TestCase):
    """Comment"""

    def setUp(self):
        """Comment"""
        self.storage = DBStorage()
        self.storage.reload()

    def tearDown(self):
        """Comment"""
        self.storage.close()
        for obj in self.storage.all().values():
            self.storage.delete(obj)
        self.storage.save()

    def test_all_with_invalid_class_type(self):
        """Comment"""
        with self.assertRaises(TypeError):
            self.storage.all(str)

    def test_count_with_invalid_class_type(self):
        with self.assertRaises(TypeError):
            self.storage.count(str)

    def test_get_with_invalid_class_type(self):
        """Comment"""
        with self.assertRaises(TypeError):
            self.storage.get(str, "fake_id")


@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
class TestDBStorageDeleteInvalidObjectType(unittest.TestCase):
    """Test deleting objects with invalid types from DBStorage"""

    def setUp(self):
        """Comment"""
        self.storage = DBStorage()
        self.storage.reload()

    def tearDown(self):
        """Comment"""
        for obj in self.storage.all().values():
            self.storage.delete(obj)
        self.storage.save()
        self.storage.close()

    def test_delete_with_invalid_object_type(self):
        """Test delete method with an invalid object type"""
        with self.assertRaises(TypeError):
            self.storage.delete("invalid_object")


@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
class TestDBStorageNewInvalidObjectType(unittest.TestCase):
    """Test creating objects with invalid types in DBStorage"""

    def setUp(self):
        """Comment"""
        self.storage = DBStorage()
        self.storage.reload()

    def tearDown(self):
        """Comment"""
        for obj in self.storage.all().values():
            self.storage.delete(obj)
        self.storage.save()
        self.storage.close()

    def test_new_with_invalid_object_type(self):
        """Test new method with an invalid object type"""
        with self.assertRaises(TypeError):
            self.storage.new("invalid_object")

# @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
# class TestDBStorageGetInvalidClassType(unittest.TestCase):
#     """Test getting objects with invalid class types in DBStorage"""
#
#     def setUp(self):
#         """Comment"""
#         self.storage = DBStorage()
#         self.storage.reload()
#
#     def tearDown(self):
#         """Comment"""
#         for obj in self.storage.all().values():
#             self.storage.delete(obj)
#         self.storage.save()
#         self.storage.close()
#
#     def test_get_with_invalid_class_type(self):
#         """Test get method with an invalid class type"""
#         with self.assertRaises(TypeError):
#             self.storage.get(str, "fake_id")
#
#
# @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
# class TestDBStorageCountInvalidClassType(unittest.TestCase):
#     """Test counting objects with invalid class types in DBStorage"""
#
#     def setUp(self):
#         """Comment"""
#         self.storage = DBStorage()
#         self.storage.reload()
#
#     def tearDown(self):
#         """Comment"""
#         for obj in self.storage.all().values():
#             self.storage.delete(obj)
#         self.storage.save()
#         self.storage.close()
#
#     def test_count_with_invalid_class_type(self):
#         """Test count method with an invalid class type"""
#         with self.assertRaises(TypeError):
#             self.storage.count(str)
