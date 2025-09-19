# The systems.py file implements the CarRentalSystem class, which acts as the central controller for managing the car rental application.
# It uses the Singleton pattern to ensure a single instance of the system, coordinating interactions between users (Customers and Admins), cars, rentals, and the database.
# The class encapsulates business logic for user registration, login, car management, rental booking, and rental management, providing a structured interface to handle user actions.
# This file integrates with other modules (models, database, utilities) to create a cohesive, object-oriented system that meets the requirements of a car rental service, including error handling and basic user-friendly features.
import hashlib
from models import Admin, Customer
from database import Database
from utilities import validate_date, notify_user, get_valid_input

class CarRentalSystem:
    """Singleton class managing the car rental system with differentiated roles."""
    _instance = None

    def __new__(cls):
        """Ensure single instance with DB connection."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.db = Database.get_instance()
        return cls._instance

    def register_user(self, username, password, role='customer'):
        """Register a user with hashed password and role."""
        try:
            if not username or not password:
                raise ValueError("Username and password are required.")
            hashed = hashlib.sha256(password.encode()).hexdigest()
            self.db.execute_query("INSERT INTO users VALUES (?, ?, ?)", (username, hashed, role))
            print(f"{role.capitalize()} registered successfully.")
        except Exception as e:
            print(f"Registration failed: {e}")

    def login(self, username, password):
        """Authenticate and return user object based on role."""
        try:
            hashed = hashlib.sha256(password.encode()).hexdigest()
            cursor = self.db.execute_query("SELECT role FROM users WHERE username = ? AND password = ?", (username, hashed))
            result = cursor.fetchone()
            if result:
                role = result[0]
                if role == 'admin':
                    return Admin(username, password)
                return Customer(username, password)
            print("Invalid credentials.")
            return None
        except Exception as e:
            print(f"Login error: {e}")
            return None

    def handle_user_action(self, user, choice):
        """Handle actions based on user role and choice."""
        try:
            if isinstance(user, Customer):
                if choice == 2:  # Book Rental
                    user.view_cars()
                    car_id = get_valid_input("Car ID: ", int)
                    start = get_valid_input("Start date (YYYY-MM-DD): ", str, validate_date)
                    end = get_valid_input("End date (YYYY-MM-DD): ", str, validate_date)
                    self.book_rental(user._username, car_id, start, end)
                elif choice == 3:  # View My Rentals
                    self.view_my_rentals(user._username)
                elif choice == 4:  # Cancel Rental
                    rental_id = get_valid_input("Rental ID: ", int)
                    user.cancel_rental(rental_id)
            elif isinstance(user, Admin):
                if choice == 1:  # Add Car
                    make = get_valid_input("Make: ", str)
                    model = get_valid_input("Model: ", str)
                    year = get_valid_input("Year: ", int)
                    mileage = get_valid_input("Mileage: ", float)
                    min_rent = get_valid_input("Min rent days: ", int)
                    max_rent = get_valid_input("Max rent days: ", int)
                    daily_rate = get_valid_input("Daily rate: ", float)
                    self.add_car(make, model, year, mileage, min_rent, max_rent, daily_rate)
                elif choice == 2:  # Update Car
                    car_id = get_valid_input("Car ID: ", int)
                    daily_rate = get_valid_input("New daily rate: ", float)
                    self.update_car(car_id, daily_rate=daily_rate)
                elif choice == 3:  # Delete Car
                    car_id = get_valid_input("Car ID: ", int)
                    if input("Confirm delete (y/n): ").lower() == 'y':
                        self.delete_car(car_id)
                elif choice == 4:  # Manage Rental
                    rental_id = get_valid_input("Rental ID: ", int)
                    status = get_valid_input("approve or reject: ", str, lambda s: s in ['approve', 'reject'])
                    self.manage_rental(rental_id, status)
                elif choice == 5:  # View Users
                    self.view_users()
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Action failed: {e}")

    def add_car(self, make, model, year, mileage, min_rent, max_rent, daily_rate):
        """Add a new car (Admin privilege)."""
        try:
            cursor = self.db.execute_query("SELECT MAX(id) FROM cars")
            car_id = (cursor.fetchone()[0] or 0) + 1
            self.db.execute_query("INSERT INTO cars VALUES (?, ?, ?, ?, ?, 1, ?, ?, ?)",
                                  (car_id, make, model, year, mileage, min_rent, max_rent, daily_rate))
            print("Car added successfully.")
        except Exception as e:
            print(f"Error adding car: {e}")

    def update_car(self, car_id, **kwargs):
        """Update car details (Admin privilege)."""
        try:
            set_clause = ', '.join(f"{k} = ?" for k in kwargs)
            params = list(kwargs.values()) + [car_id]
            self.db.execute_query(f"UPDATE cars SET {set_clause} WHERE id = ?", params)
            print("Car updated successfully.")
        except Exception as e:
            print(f"Error updating car: {e}")

    def delete_car(self, car_id):
        """Delete a car (Admin privilege)."""
        try:
            if self.db.execute_query("SELECT * FROM rentals WHERE car_id = ? AND status NOT IN ('rejected', 'cancelled')", (car_id,)).fetchall():
                print("Cannot delete car with active rental.")
                return
            self.db.execute_query("DELETE FROM cars WHERE id = ?", (car_id,))
            print("Car deleted successfully.")
        except Exception as e:
            print(f"Error deleting car: {e}")

    def view_available_cars(self):
        """View available cars (Customer privilege)."""
        cursor = self.db.execute_query("SELECT * FROM cars WHERE available = 1")
        cars = cursor.fetchall()
        if not cars:
            print("No cars available.")
            return
        for car in cars:
            print(f"ID: {car[0]}, Make: {car[1]}, Model: {car[2]}, Year: {car[3]}, Mileage: {car[4]}, Min/Max Rent: {car[6]}-{car[7]} days, Daily Rate: ${car[8]}")

    def book_rental(self, customer, car_id, start_date, end_date):
        """Book a rental (Customer privilege) with fee calculation."""
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
                print(f"Rental must be between {car[6]} and {car[7]} days.")
                return
            # Conflict check
            conflicts = self.db.execute_query("SELECT * FROM rentals WHERE car_id = ? AND status NOT IN ('rejected', 'cancelled') AND ((start_date <= ? AND end_date >= ?) OR (start_date <= ? AND end_date >= ?))",
                                              (car_id, end_date, start_date, start_date, end_date)).fetchall()
            if conflicts:
                print("Date conflict with existing booking.")
                return
            fee = days * car[8]
            if input("Add insurance ($10/day)? (y/n): ").lower() == 'y':
                fee += 10 * days
            cursor = self.db.execute_query("SELECT MAX(id) FROM rentals")
            rental_id = (cursor.fetchone()[0] or 0) + 1
            self.db.execute_query("INSERT INTO rentals VALUES (?, ?, ?, ?, ?, 'pending', ?)",
                                  (rental_id, customer, car_id, start_date, end_date, fee))
            self.db.execute_query("UPDATE cars SET available = 0 WHERE id = ?", (car_id,))
            print(f"Booking created (pending). Total fee: ${fee}")
        except ValueError:
            print("Invalid date format.")
        except Exception as e:
            print(f"Error booking rental: {e}")

    def manage_rental(self, rental_id, status):
        """Manage rental status (Admin privilege)."""
        try:
            if status not in ['approve', 'reject']:
                print("Status must be 'approve' or 'reject'.")
                return
            self.db.execute_query("UPDATE rentals SET status = ? WHERE id = ?", (status, rental_id))
            if status == 'reject':
                cursor = self.db.execute_query("SELECT car_id FROM rentals WHERE id = ?", (rental_id,))
                car_id = cursor.fetchone()[0]
                self.db.execute_query("UPDATE cars SET available = 1 WHERE id = ?", (car_id,))
            cursor = self.db.execute_query("SELECT customer FROM rentals WHERE id = ?", (rental_id,))
            customer = cursor.fetchone()[0]
            notify_user(customer, f"Your rental ID {rental_id} has been {status}.")
            print("Rental managed successfully.")
        except Exception as e:
            print(f"Error managing rental: {e}")

    def view_my_rentals(self, customer):
        """View customer's rentals (Customer privilege)."""
        cursor = self.db.execute_query("SELECT * FROM rentals WHERE customer = ?", (customer,))
        rentals = cursor.fetchall()
        if not rentals:
            print("No rentals found.")
            return
        for rental in rentals:
            print(f"ID: {rental[0]}, Car ID: {rental[2]}, Start: {rental[3]}, End: {rental[4]}, Status: {rental[5]}, Fee: ${rental[6]}")

    def view_users(self):
        """View all users (Admin privilege)."""
        cursor = self.db.execute_query("SELECT username, password, role FROM users")
        users = cursor.fetchall()
        if not users:
            print("No users found.")
            return
        for user in users:
            print(f"Username: {user[0]}, Password: {user[1]}, Role: {user[2]}")