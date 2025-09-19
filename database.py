import sqlite3
import json
import hashlib


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect('car_rental.db')
            cls._instance._setup_tables()
        return cls._instance

    def _setup_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, role TEXT)')
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS cars (id INTEGER PRIMARY KEY AUTOINCREMENT, make TEXT, model TEXT, year INTEGER, mileage REAL, available INTEGER, min_rent INTEGER, max_rent INTEGER, daily_rate REAL)')
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS rentals (id INTEGER PRIMARY KEY, customer TEXT, car_id INTEGER, start_date TEXT, end_date TEXT, status TEXT, fee REAL)')

        # Clear existing cars to avoid duplicate ID conflicts (optional, comment out if not needed)
        cursor.execute("DELETE FROM cars")

        # Load and insert initial car data from base_cars.json
        try:
            with open('base_cars.json', 'r') as file:
                cars = json.load(file)
                for car in cars:  # Omit id, let AUTOINCREMENT handle it
                    cursor.execute(
                        "INSERT INTO cars (make, model, year, mileage, available, min_rent, max_rent, daily_rate) VALUES (?, ?, ?, ?, 1, ?, ?, ?)",
                        (car['make'], car['model'], car['year'], car['mileage'], car['min_rent'], car['max_rent'],
                         car['daily_rate']))
            self.conn.commit()
        except FileNotFoundError:
            print("Warning: base_cars.json not found, no initial cars loaded.")
        except Exception as e:
            print(f"Error loading initial cars: {e}")

        # Pre-create admin account if it doesn't exist
        admin_password_hash = hashlib.sha256("Abc123".encode()).hexdigest()
        cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", ('CS_Manager', admin_password_hash, 'admin'))
        self.conn.commit()

    def execute_query(self, sql, params=()):
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        self.conn.commit()
        return cursor

    @classmethod
    def get_instance(cls):
        return cls()