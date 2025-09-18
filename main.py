import models
from systems import CarRentalSystem

def main():
    """Main entry point for the car rental system."""
    system = CarRentalSystem()  # Singleton instance
    while True:
        print("\nCar Rental System")
        print("1. Register\n2. Login\n3. Exit")
        choice = input("Choose: ").strip()
        if choice == '3':
            break
        if choice == '1':
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            role = input("Role (customer/admin): ").strip().lower()
            if role in ['customer', 'admin']:
                system.register_user(username, password, role)
            else:
                print("Invalid role.")
        elif choice == '2':
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            user = system.login(username, password)
            if user:
                while True:
                    if isinstance(user, models.Customer):
                        print("\nCustomer Menu")
                        print("1. View/Search Cars\n2. Book Rental\n3. View My Rentals\n4. Cancel Rental\n5. Logout")
                        c = input("Choose: ").strip()
                        if c == '5':
                            break
                        elif c == '1':
                            criteria = {'make': input("press Enter: ").strip() or None}
                            user.search_cars(criteria)
                        elif c in ['2', '3', '4']:
                            system.handle_user_action(user, int(c))
                    elif isinstance(user, models.Admin):
                        print("\nAdmin Menu")
                        print("1. Add Car\n2. Update Car\n3. Delete Car\n4. Manage Rental\n5. View Users\n6. Logout")
                        c = input("Choose: ").strip()
                        if c == '6':
                            break
                        system.handle_user_action(user, int(c))

if __name__ == "__main__":
    main()