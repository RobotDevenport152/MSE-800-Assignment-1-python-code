from models import User, Admin, Customer, Car, Rental
from database import Database
from utilities import validate_date, notify_user, get_valid_input

class CarRentalSystem:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.db = Database.get_instance()
        return cls._instance

    def register_user(self, username, password, role='customer'):
        try:
            self.db.execute_query("INSERT INTO users VALUES (?, ?, ?)", (username, password, role))
            print("Registered successfully.")
        except Exception as e:
            print(f"Registration failed: {e}")

    def login(self, username, password):
        cursor = self.db.execute_query("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        if result:
            role = result[0]
            if role == 'admin':
                return Admin(username, password)
            return Customer(username, password)
        print("Invalid credentials.")
        return None

    def handle_user_action(self, user, choice):
        if isinstance(user, Customer):
            if choice == 1:
                self.view_available_cars()
            elif choice == 2:
                car_id = int(get_valid_input("Car ID: ", int))
                start = get_valid_input("Start date (YYYY-MM-DD): ", str, validate_date)
                end = get_valid_input("End date (YYYY-MM-DD): ", str, validate_date)
                self.book_rental(user._username, car_id, start, end)
            elif choice == 3:
                self.view_my_rentals(user._username)
        elif isinstance(user, Admin):
            if choice == 1:
                make = get_valid_input("Make: ", str)
                model = get_valid_input("Model: ", str)
                year = get_valid_input("Year: ", int)
                mileage = get_valid_input("Mileage: ", float)
                min_rent = get_valid_input("Min rent days: ", int)
                max_rent = get_valid_input("Max rent days: ", int)
                daily_rate = get_valid_input("Daily rate: ", float)
                self.add_car(make, model, year, mileage, min_rent, max_rent, daily_rate)
            elif choice == 2:
                car_id = get_valid_input("Car ID: ", int)
                daily_rate = get_valid_input("New daily rate: ", float)
                self.update_car(car_id, daily_rate=daily_rate)
            elif choice == 3:
                car_id = get_valid_input("Car ID: ", int)
                self.delete_car(car_id)
            elif choice == 4:
                rental_id = get_valid_input("Rental ID: ", int)
                status = get_valid_input("Approve or reject: ", str, lambda s: s in ['approve', 'reject'])
                self.manage_rental(rental_id, status)

    def add_car(self, make, model, year, mileage, min_rent, max_rent, daily_rate):
        try:
            cursor = self.db.execute_query("SELECT MAX(id) FROM cars")
            car_id = (cursor.fetchone()[0] or 0) + 1
            self.db.execute_query("INSERT INTO cars VALUES (?, ?, ?, ?, ?, 1, ?, ?, ?)",
                                  (car_id, make, model, year, mileage, min_rent, max_rent, daily_rate))
            print("Car added.")
        except Exception as e:
            print(f"Error adding car: {e}")

    def update_car(self, car_id, **kwargs):
        try:
            set_clause = ', '.join(f"{k} = ?" for k in kwargs)
            params = list(kwargs.values()) + [car_id]
            self.db.execute_query(f"UPDATE cars SET {set_clause} WHERE id = ?", params)
            print("Car updated.")
        except Exception as e:
            print(f"Error updating car: {e}")

    def delete_car(self, car_id):
        try:
            self.db.execute_query("DELETE FROM cars WHERE id = ?", (car_id,))
            print("Car deleted.")
        except Exception as e:
            print(f"Error deleting car: {e}")

    def view_available_cars(self):
        cursor = self.db.execute_query("SELECT * FROM cars WHERE available = 1")
        for row in cursor.fetchall():
            print(f"ID: {row[0]}, Make: {row[1]}, Model: {row[2]}, Year: {row[3]}, Mileage: {row[4]}, Daily Rate: {row[8]}")

    def book_rental(self, customer, car_id, start_date, end_date):
        try:
            from datetime import datetime
            cursor = self.db.execute_query("SELECT * FROM cars WHERE id = ? AND available = 1", (car_id,))
            car = cursor.fetchone()
            if not car:
                print("Car not available.")
                return
            start_d = datetime.strptime(start_date, "%Y-%m-%d")
            end_d = datetime.strptime(end_date, "%Y-%m-%d")
            days = (end_d - start_d).days
            if days < car[6] or days > car[7]:
                print("Invalid rental period.")
                return
            fee = days * car[8]
            cursor = self.db.execute_query("SELECT MAX(id) FROM rentals")
            rental_id = (cursor.fetchone()[0] or 0) + 1
            self.db.execute_query("INSERT INTO rentals VALUES (?, ?, ?, ?, ?, 'pending', ?)",
                                  (rental_id, customer, car_id, start_date, end_date, fee))
            self.db.execute_query("UPDATE cars SET available = 0 WHERE id = ?", (car_id,))
            print("Booking created (pending).")
            print("Recommendation: Consider insurance for longer rentals!")
        except Exception as e:
            print(f"Error booking rental: {e}")

    def manage_rental(self, rental_id, status):
        try:
            self.db.execute_query("UPDATE rentals SET status = ? WHERE id = ?", (status, rental_id))
            if status == "reject":
                cursor = self.db.execute_query("SELECT car_id FROM rentals WHERE id = ?", (rental_id,))
                car_id = cursor.fetchone()[0]
                self.db.execute_query("UPDATE cars SET available = 1 WHERE id = ?", (car_id,))
            cursor = self.db.execute_query("SELECT customer FROM rentals WHERE id = ?", (rental_id,))
            customer = cursor.fetchone()[0]
            notify_user(customer, f"Your rental ID {rental_id} has been {status}.")
            print("Rental managed.")
        except Exception as e:
            print(f"Error managing rental: {e}")

    def view_my_rentals(self, customer):
        cursor = self.db.execute_query("SELECT * FROM rentals WHERE customer = ?", (customer,))
        for row in cursor.fetchall():
            print(f"ID: {row[0]}, Car ID: {row[2]}, Status: {row[4]}, Fee: {row[6]}")