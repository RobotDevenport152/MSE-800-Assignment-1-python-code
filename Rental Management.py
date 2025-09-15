from datetime import datetime
class Rental:
    def __init__(self, id, customer, car, start_date, end_date):
        self.id = id
        self.customer = customer.username  # Store username for serialization
        self.car = car
        self.car_id = car.id  # For reference
        self.start_date = start_date
        self.end_date = end_date
        self.status = "pending"
        self.fee = self.calculate_fee()
        self.observers = []
        car.available = False  # Mark as unavailable temporarily

    def calculate_fee(self):
        """Calculate rental fee."""
        start = datetime.strptime(self.start_date, "%Y-%m-%d")
        end = datetime.strptime(self.end_date, "%Y-%m-%d")
        days = (end - start).days
        return self.car.daily_rate * days