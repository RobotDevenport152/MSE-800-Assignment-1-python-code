import sqlite3
import json

class Database:
    _instance = None

    def __init__(self):
        if not Database._instance:
            self.conn = sqlite3.connect('car_rental.db')
            self._setup_tables()
            Database._instance = self

    @staticmethod
    def get_instance():
        if not Database._instance:
            Database()
        return Database._instance

    def _setup_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY, password TEXT, role TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY, make TEXT, model TEXT, year INTEGER, mileage REAL,
            available INTEGER, min_rent INTEGER, max_rent INTEGER, daily_rate REAL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS rentals (
            id INTEGER PRIMARY KEY, customer TEXT, car_id INTEGER, start_date TEXT,
            end_date TEXT, status TEXT, fee REAL)''')
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO users VALUES ('CS_Manager', 'Abc123', 'admin')")
            cursor.execute("INSERT INTO users VALUES ('test', 'test', 'customer')")
        cursor.execute("SELECT COUNT(*) FROM cars")
        if cursor.fetchone()[0] == 0:
            with open('base_cars.json', 'r') as f:
                cars = json.load(f)
            for car in cars:
                cursor.execute("INSERT INTO cars VALUES (NULL, ?, ?, ?, ?, 1, ?, ?, ?)",
                               (car['make'], car['model'], car['year'], car['mileage'], car['min_rent'], car['max_rent'], car['daily_rate']))
        self.conn.commit()

    def execute_query(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor