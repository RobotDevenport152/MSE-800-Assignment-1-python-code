class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password  # Note: In production, hash this
        self.role = role

    def login(self, username, password):
        """Check login credentials."""
        return self.username == username and self.password == password

class Customer(User):
    """
    Customer user class, inherits from User. Acts as Observer for notifications.
    """
    def __init__(self, username, password):
        super().__init__(username, password, "customer")

    def view_cars(self):
        """View available cars (calls DataManager)."""
        from services.data_manager import DataManager
        cars = DataManager.get_instance().get_available_cars()
        for car in cars:
            print(f"ID: {car['id']}, Make: {car['make']}, Model: {car['model']}, Year: {car['year']}, Available: {car['available']}")

    def book_car(self, car_id, start_date, end_date):
        """Book a car (creates rental)."""
        from models.rental import Rental
        from datetime import datetime
        dm = DataManager.get_instance()
        car_data = next((c for c in dm.cars if c['id'] == car_id and c['available']), None)
        if not car_data:
            print("Car not available.")
            return
        # Convert strings to dates
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        days = (end - start).days
        if days < car_data['min_rent'] or days > car_data['max_rent']:
            print("Invalid rental period.")
            return
        car = Car(**car_data)  # Rehydrate to object
        rental = Rental(dm.next_rental_id, self, car, start_date, end_date)
        dm.next_rental_id += 1
        dm.add_rental(rental)
        rental.attach(self)  # Attach as observer
        print("Booking created (pending).")

    def update(self, message):
        """Observer update method for notifications."""
        print(f"Notification for {self.username}: {message}")

class Admin(User):
    """
    Admin user class, inherits from User.
    """
    def __init__(self, username, password):
        super().__init__(username, password, "admin")

    def add_car(self, make, model, year, mileage, daily_rate, min_rent, max_rent):
        """Add a new car."""
        car = Car(dm.next_car_id, make, model, year, mileage, daily_rate, min_rent, max_rent)
        dm.next_car_id += 1
        dm.add_car(car.__dict__)
        print("Car added.")

    def update_car(self, car_id, **kwargs):
        """Update car details."""
        DataManager.get_instance().update_car(car_id, **kwargs)
        print("Car updated.")

    def delete_car(self, car_id):
        """Delete a car."""
        DataManager.get_instance().delete_car(car_id)
        print("Car deleted.")

    def manage_rentals(self):
        """View and manage rentals."""
        rentals = dm.get_rentals()
        for r in rentals:
            print(f"ID: {r['id']}, Customer: {r['customer']}, Car: {r['car_id']}, Status: {r['status']}")
        rental_id = int(input("Enter rental ID to manage: "))
        status = input("Enter new status (approved/rejected): ")
        dm.update_rental_status(rental_id, status)

