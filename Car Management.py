class Car:
    """
    Car class representing a vehicle.
    """
    def __init__(self, id, make, model, year, mileage, daily_rate, min_rent, max_rent):
        self.id = id
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.available = True
        self.daily_rate = daily_rate
        self.min_rent = min_rent
        self.max_rent = max_rent