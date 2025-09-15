Car Rental System
This is a Python-based command-line user interface for managing car rental
operations. The system follows object-oriented design principles and implements
the Singleton pattern to ensure system uniqueness.
No manual configurations are needed to run the project,
requirements.txt is attached.

How to run:
1. Ensure Python 3.10 or higher is installed, tested on Python 3.13.
2. Install required dependencies: pip install -r requirements.txt.
3. Run the main file from the command line: python main.py.
4. Follow the instructions in the console to operate the system.

All relavant files included:
• main.py: Main entry point of the application, handling the user interface
and menu interactions.
• system.py: Core business logic, including management of users, vehicles,
and rentals.
• models.py: Defines all classes (User, Admin, Customer, Car, Rental),
demonstrating object-oriented design.
• utilities.py: Contains various utility functions, such as input validation
and screen clearing.
• database.py: Provides an interface for all database operations using
SQLite.
• base_cars.json: JSON file containing initial vehicle data.
• requirements.txt: Lists all project dependencies.

NOTE:
A default administrator is created when the project starts. Default credentials:
Username: CS_Manager Password: Abc123
A test user is created when doing test runs. Test user credentials: Username:
test Password: test

License terms
This project is released under the MIT License. Allows users to freely use, copy,
modify, distribute, sublicense the software, as long as proper credit is given.

Test runs show no known bugs at the moment.

Credits
Developer: Junbin Xu, Master of Software Engineering, Yoobee Colleges, Auckland