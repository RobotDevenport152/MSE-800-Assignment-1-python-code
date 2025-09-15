from systems import CarRentalSystem
from utilities import clear_screen, get_valid_input

def main():
    system = CarRentalSystem()
    while True:
        clear_screen()
        print("\nCar Rental System")
        print("1. Register (Customer)")
        print("2. Login")
        print("3. Exit")
        choice = get_valid_input("Choose: ", str)
        if choice == "3":
            break
        elif choice == "1":
            username = get_valid_input("Username: ", str)
            password = get_valid_input("Password: ", str)
            system.register_user(username, password, 'customer')
        elif choice == "2":
            username = get_valid_input("Username: ", str)
            password = get_valid_input("Password: ", str)
            user = system.login(username, password)
            if user:
                while True:
                    clear_screen()
                    options = user.get_menu_options()
                    for i, opt in enumerate(options, 1):
                        print(f"{i}. {opt}")
                    print(f"{len(options) + 1}. Logout")
                    sub_choice = get_valid_input("Choose: ", int, lambda x:x in range(1, len(options) + 2))
                    if sub_choice == len(options) + 1:
                        break
                    system.handle_user_action(user, sub_choice)

if __name__ == "__main__":
    main()