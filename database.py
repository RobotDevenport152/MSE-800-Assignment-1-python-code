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
        # Insert initial car data
        initial_cars = [
            ('Toyota', 'Camry', 2020, 5000.0, 1, 30, 50.0),
            ('Honda', 'Civic', 2019, 8000.0, 2, 15, 40.0),
            ('Ford', 'Focus', 2021, 3000.0, 1, 20, 45.0),
            ('Chevrolet', 'Malibu', 2020, 6000.0, 3, 25, 48.0),
            ('Nissan', 'Altima', 2019, 10000.0, 2, 18, 42.0),
            ('BMW', '3 Series', 2021, 4000.0, 1, 10, 80.0),
            ('Mercedes-Benz', 'C-Class', 2020, 7000.0, 2, 12, 85.0),
            ('Hyundai', 'Elantra', 2018, 12000.0, 1, 25, 38.0),
            ('Kia', 'Optima', 2019, 9500.0, 2, 20, 44.0),
            ('Tesla', 'Model 3', 2022, 1500.0, 1, 7, 100.0)
        ]
        with open('base_cars.json', 'r') as file:
            cars = json.load(file)
            for i, car in enumerate(cars, 1):
                cursor.execute("INSERT OR IGNORE INTO cars VALUES (?, ?, ?, ?, ?, 1, ?, ?, ?)",
                               (i, car['make'], car['model'], car['year'], car['mileage'], car['min_rent'],
                                car['max_rent'], car['daily_rate']))
        self.conn.commit()
        self.conn.commit()

    def execute_query(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor