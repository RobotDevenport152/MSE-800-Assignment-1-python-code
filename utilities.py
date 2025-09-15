import os
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_valid_input(prompt, type_, validator=None):
    while True:
        try:
            value = type_(input(prompt))
            if validator and not validator(value):
                raise ValueError("Invalid input.")
            return value
        except ValueError as e:
            print(f"Error: {e}. Try again.")

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def notify_user(customer, message):
    print(f"Notification for {customer}: {message}")