# Bank Management System with Python

#### Video Demo:  (https://www.youtube.com/watch?v=FOnoPoAQ2lU)

## Description:

- This implementation was created as the final project for the CS50’s Introduction to Programming with Python course offered remotely and for free by Harvard University and the edX platform. The course focuses entirely on the Python language, covering topics such as conditional and loop structures, file handling and external libraries, exception handling, unit testing, regular expressions, and object-oriented programming (OOP). It includes numerous exercises inspired by real-world programming problems.
- The project consists of a comprehensive Bank Management System built with Python, designed to manage accounts, transactions, and user authentication efficiently. The project is divided into distinct modules (account.py, client.py, helper.py, project.py) to promote code reusability and maintainability. Data is saved after program usage in files in the same directory as the project. The choice to use JSON and CSV for data persistence is due to their simplicity and human-readability. JSON is used to save detailed account information, while CSV is used for credentials. A simple authentication system using usernames and passwords was implemented to demonstrate basic security principles. Finally, the pytest library is used for unit testing to ensure the reliability of the system through automated tests.
- An important note: as I am Brazilian, I chose to use the Brazilian monetary system for string formatting in reais (R$), and we also use CPF (Cadastro de Pessoas Físicas) as an attribute of clients, which is a 9-digit number that is the main identification document for individuals in Brazil.

## Features

- **Account Management**: Create and manage user accounts.
- **Transactions**: Handle deposits, withdrawals, and transfers.
- **Authentication**: Secure login system with username and password.
- **Data Persistence**: Save and load account data using JSON and CSV files.
- **Statements**: Generate account statements with transaction history.

## Files Descriptions

- **account.py**: Contains the Account class, which defines the structure and methods for managing bank accounts, including deposits, withdrawals, transfers, and generating statements.
- **client.py**: Contains the Client class, which stores client information such as name and CPF.
- **helper.py**: Provides helper functions like format_float_to_currency_str for formatting currency values. And others to convert datetime objects to strings and vice versa.
- **project.py**: The main application script that handles user interactions, account creation, login, and various banking operations. It also includes functions for loading and saving account data.
- **test_project.py**: Contains unit tests for verifying the functionality of the account management system, including account creation, login, deposits, withdrawals, and transfers.
- **usernames.csv**: File where login information (usernames and passwords) will be saved.
- **accounts.json**: File where information about the accounts created in the system will be saved.
- **requirements.txt**: Lists the project's dependencies, primarily pytest for testing.

## Requirements

To run the project and execute the tests, you need to have pytest installed. You can install it via pip using the following command:

pip install -r requirements.txt

## Testing

This project uses pytest for testing. To run the tests, execute the following command:

pytest test_project.py
 