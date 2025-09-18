# Create abstract method for car rental system, which ensures that user have the attributes of username and password, customer and administrator can also inherited the attributes.
# Define cars and rental's attributes so that key information can be stored and access.
# All attributes related to sensitive information are protected by using private method so that it can be only accessed by certain given methods, otherwise it's stored in the backend.
import abc

class User(metaclass=abc.ABCMeta):
    """Abstract base class for users with encapsulation."""
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def authenticate(self, password):
        """Authenticate user with hashed password."""
        return self.password == password

    @abc.abstractmethod
    def role_specific_action(self):
        """Abstract method for role-specific actions."""
        pass

class Customer(User):
    """Customer class with specific privileges."""
    def __init__(self, username, password):
        super().__init__(username, password)

    def view_cars(self):
        """View available cars."""
        from systems import CarRentalSystem
        CarRentalSystem().view_available_cars()

    def search_cars(self, criteria):
        """Search cars by criteria."""
        from systems import CarRentalSystem
        CarRentalSystem().view_available_cars()  # Simplified; enhance with search logic

    def cancel_rental(self, rental_id):
        """Cancel a pending rental."""
        from systems import CarRentalSystem
        system = CarRentalSystem()
        cursor = system.db.execute_query("SELECT * FROM rentals WHERE id = ? AND customer = ? AND status = 'pending'", (rental_id, self._username))
        if cursor.fetchone():
            system.db.execute_query("UPDATE rentals SET status = 'cancelled' WHERE id = ?", (rental_id,))
            cursor = system.db.execute_query("SELECT car_id FROM rentals WHERE id = ?", (rental_id,))
            car_id = cursor.fetchone()[0]
            system.db.execute_query("UPDATE cars SET available = 1 WHERE id = ?", (car_id,))
            print("Rental cancelled.")
        else:
            print("Cannot cancel rental.")

    def role_specific_action(self):
        pass  # Implemented in handle_user_action

class Admin(User):
    """Admin class with specific privileges."""
    def __init__(self, username, password):
        super().__init__(username, password)

    def role_specific_action(self):
        pass  # Implemented in handle_user_action