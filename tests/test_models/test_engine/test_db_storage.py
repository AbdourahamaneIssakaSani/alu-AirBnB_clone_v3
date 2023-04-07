#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""
import random
import uuid
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

from tests.test_models.test_base_model import TestBaseModel

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
class TestDBStorageGetCity(unittest.TestCase):
    """Tests get method of the DBStorage class for the City class"""

    def setUp(self):
        """Set up for the tests"""

        self.storage = DBStorage()
        self.storage.reload()
        self.new_state = State(name="California")
        self.new_state.save()
        self.new_city1 = City(name="San Francisco", state_id=self.new_state.id)
        self.new_city2 = City(name="Los Angeles", state_id=self.new_state.id)
        self.new_city1.save()
        self.new_city2.save()

    def tearDown(self):
        """Tear down after the tests"""

        self.storage.delete(self.new_city1)
        self.storage.delete(self.new_city2)
        self.storage.delete(self.new_state)
        self.storage.save()
        self.storage.close()

    def test_get_existing_city(self):
        """Test get() with an existing City object"""
        obj = self.storage.get(City, self.new_city1.id)
        self.assertEqual(obj.id, self.new_city1.id)

    def test_get_nonexistent_city(self):
        """Test get() with a nonexistent City object"""
        obj = self.storage.get(City, "nonexistent")
        self.assertIsNone(obj)


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "skip if not db")
class TestDBStorageCountCity(unittest.TestCase):
    """Tests the count() method of the DBStorage class for the City class"""

    def setUp(self):
        """Set up for the tests"""

        self.storage = DBStorage()
        self.storage.reload()
        self.new_state = State(name="California")
        self.new_state.save()
        self.new_city1 = City(name="San Francisco", state_id=self.new_state.id)
        self.new_city2 = City(name="Los Angeles", state_id=self.new_state.id)
        self.new_city1.save()
        self.new_city2.save()

    def tearDown(self):
        """Tear down after the tests"""

        self.storage.delete(self.new_city1)
        self.storage.delete(self.new_city2)
        self.storage.delete(self.new_state)
        self.storage.save()
        self.storage.close()

    def test_count_all_city_objects(self):
        """Test count() with no arguments for City class"""
        count = self.storage.count()
        self.assertEqual(count, 3)

    def test_count_some_city_objects(self):
        """Test count() with a class argument for City class"""
        count = self.storage.count(City)
        self.assertEqual(count, 2)

    def test_count_nonexistent_city_class(self):
        """Test count() with a nonexistent class argument for City class"""
        count = self.storage.count(Amenity)
        self.assertEqual(count, 0)


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "skip if not db")
class TestDBStorageCreateAndUpdate(unittest.TestCase):
    """Tests for creating and updating objects with DBStorage"""

    def setUp(self):
        """Set up for the tests"""
        self.storage = DBStorage()
        self.storage.reload()
        self.new_state = State(name="Test State")
        self.storage.new(self.new_state)
        self.storage.save()

    def tearDown(self):
        """Tear down after the tests"""
        self.storage.delete(self.new_state)
        self.storage.save()
        self.storage.close()

    def test_create_state(self):
        """Test creating a new State object and saving it to the database"""
        retrieved_state = self.storage.get(State, self.new_state.id)
        self.assertIsNotNone(retrieved_state)
        self.assertEqual(retrieved_state.name, "Test State")

    def test_update_state(self):
        """Test updating an existing State object and saving the
        changes to the database"""
        self.new_state.name = "Updated Test State"
        self.storage.save()

        retrieved_state = self.storage.get(State, self.new_state.id)
        self.assertIsNotNone(retrieved_state)
        self.assertEqual(retrieved_state.name, "Updated Test State")

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
        new_city = City(name="Test City", state_id=self.new_state.id)
        self.storage.new(new_city)
        self.storage.save()

        retrieved_city = self.storage.get(City, new_city.id)
        self.assertIsNotNone(retrieved_city)
        self.assertEqual(retrieved_city.state_id, self.new_state.id)

        retrieved_state = self.storage.get(State, self.new_state.id)
        self.assertIsNotNone(retrieved_state)

        self.assertIn(new_city, retrieved_state.cities)

        self.storage.delete(new_city)
        self.storage.save()


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "skip if not db")
class TestDBStorageGetUser(unittest.TestCase):
    """Tests get method of the DBStorage class for the User class"""

    def setUp(self):
        """Set up for the tests"""

        self.storage = DBStorage()
        self.storage.reload()
        self.new_user1 = User(email="user1@example.com", password="password1")
        self.new_user2 = User(email="user2@example.com", password="password2")
        self.new_user1.save()
        self.new_user2.save()

    def tearDown(self):
        """Tear down after the tests"""

        self.storage.delete(self.new_user1)
        self.storage.delete(self.new_user2)
        self.storage.save()
        self.storage.close()

    def test_get_existing_user(self):
        """Test get() with an existing User object"""
        obj = self.storage.get(User, self.new_user1.id)
        self.assertEqual(obj.id, self.new_user1.id)

    def test_get_nonexistent_user(self):
        """Test get() with a nonexistent User object"""
        obj = self.storage.get(User, "nonexistent")
        self.assertIsNone(obj)


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "skip if not db")
class TestDBStorageCountUser(unittest.TestCase):
    """Tests the count() method of the DBStorage class for the User class"""

    def setUp(self):
        """Set up for the tests"""

        self.storage = DBStorage()
        self.storage.reload()
        self.new_user1 = User(email="user1@example.com", password="password1")
        self.new_user2 = User(email="user2@example.com", password="password2")
        self.new_user1.save()
        self.new_user2.save()

    def tearDown(self):
        """Tear down after the tests"""

        self.storage.delete(self.new_user1)
        self.storage.delete(self.new_user2)
        self.storage.save()
        self.storage.close()

    def test_count_all_user_objects(self):
        """Test count() with no arguments for User class"""
        count = self.storage.count()
        self.assertEqual(count, 2)

    def test_count_some_user_objects(self):
        """Test count() with a class argument for User class"""
        count = self.storage.count(User)
        self.assertEqual(count, 2)

    def test_count_nonexistent_user_class(self):
        """Test count() with a nonexistent class argument for User class"""
        count = self.storage.count(Amenity)
        self.assertEqual(count, 0)


class TestAmenity(TestBaseModel):
    """ Test for amenity"""

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """ """
        new = self.value()
        new.name = "amenity"
        self.assertEqual(type(new.name), str)


class TestPlace(TestBaseModel):
    """ Test for place"""

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_city_id(self):
        """ """
        new = self.value()
        city = City()
        new.city_id = city.id
        self.assertEqual(type(new.city_id), str)

    def test_user_id(self):
        """ """
        new = self.value()
        user = User()
        new.user_id = user.id
        self.assertEqual(type(new.user_id), str)

    def test_name(self):
        """ """
        new = self.value()
        new.name = "Place"
        self.assertEqual(type(new.name), str)

    def test_description(self):
        """ """
        new = self.value()
        new.description = ""
        self.assertEqual(type(new.description), str)

    def test_number_rooms(self):
        """ """
        new = self.value()
        new.number_rooms = 4
        self.assertEqual(type(new.number_rooms), int)

    def test_number_bathrooms(self):
        """ """
        new = self.value()
        new.number_bathrooms = 2
        self.assertEqual(type(new.number_bathrooms), int)

    def test_max_guest(self):
        """ """
        new = self.value()
        new.max_guest = 8
        self.assertEqual(type(new.max_guest), int)

    def test_price_by_night(self):
        """ """
        new = self.value()
        new.price_by_night = 18
        self.assertEqual(type(new.price_by_night), int)

    def test_latitude(self):
        """ """
        new = self.value()
        new.latitude = -123.085222
        self.assertEqual(type(new.latitude), float)

    def test_longitude(self):
        """ """
        new = self.value()
        new.longitude = -120.085222
        self.assertEqual(type(new.longitude), float)


class TestUserFields(unittest.TestCase):
    """Comment"""

    def setUp(self):
        """Comment"""
        self.user = User()

    def test_random_email_1(self):
        """Comment"""
        self.user.email = "test1@example.com"
        self.assertEqual(self.user.email, "test1@example.com")

    def test_random_email_2(self):
        """Comment"""
        self.user.email = "random2@test.org"
        self.assertEqual(self.user.email, "random2@test.org")

    def test_random_first_name_1(self):
        """Comment"""
        self.user.first_name = "John"
        self.assertEqual(self.user.first_name, "John")

    def test_random_first_name_2(self):
        """Comment"""
        self.user.first_name = "Jane"
        self.assertEqual(self.user.first_name, "Jane")

    def test_random_last_name_1(self):
        """Comment"""
        self.user.last_name = "Doe"
        self.assertEqual(self.user.last_name, "Doe")

    def test_random_last_name_2(self):
        """Comment"""
        self.user.last_name = "Smith"
        self.assertEqual(self.user.last_name, "Smith")

    def test_random_id_1(self):
        """Comment"""
        self.user.id = str(uuid.uuid4())
        self.assertIsInstance(self.user.id, str)

    def test_random_id_2(self):
        """Comment"""
        new_id = str(uuid.uuid4())
        self.user.id = new_id
        self.assertEqual(self.user.id, new_id)
