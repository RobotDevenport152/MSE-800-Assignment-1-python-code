# Create abstract method for car rental system, which ensures that user have the attributes of username and password, customer and administrator can also inherited the attributes.
# Define cars and rental's attributes so that key information can be stored and access.
# All attributes related to sensitive information are protected by using private method so that it can be only accessed by certain given methods, otherwise it's stored in the backend.
from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, username, password):
        self._username = username
        self._password = password

    @abstractmethod
    def get_menu_options(self):
        pass


class Customer(User):
    def get_menu_options(self):
        return ["View Available Cars", "Book Rental", "View My Rentals"]


class Admin(User):
    def get_menu_options(self):
        return ["Add Car", "Update Car", "Delete Car", "Manage Rentals"]


class Car:
    def __init__(self, **kwargs):
        self._id = kwargs.get('id')
        self._make = kwargs['make']
        self._model = kwargs['model']
        self._year = kwargs['year']
        self._mileage = kwargs['mileage']
        self._available = kwargs.get('available', True)
        self._min_rent = kwargs['min_rent']
        self._max_rent = kwargs['max_rent']
        self._daily_rate = kwargs['daily_rate']


class Rental:
    def __init__(self, **kwargs):
        self._id = kwargs.get('id')
        self._customer = kwargs['customer']
        self._car_id = kwargs['car_id']
        self._start_date = kwargs['start_date']
        self._end_date = kwargs['end_date']
        self._status = kwargs.get('status', 'pending')
        self._fee = kwargs['fee']