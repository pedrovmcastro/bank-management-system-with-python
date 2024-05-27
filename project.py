"""
BANK MANAGEMENT SYSTEM

Name: Pedro Vitor Marques de Castro
GitHub username: pedrovmcastro
edX username: pvmcastro
City: Campinas, SP
Country: Brazil
Recorded in: 2024-05-27
"""

from account import Account
from client import Client
from helper import format_float_to_currency_str

from sys import exit
import getpass
from typing import Union
import csv
import json

accounts = {}

def main() -> None:
    global accounts
    load_accounts()
    while True:
        print("╔════════════════════════════════════╗")
        print("║          Welcome to the Bank!      ║")
        print("║                                    ║")
        print("║          1. Create Account         ║")
        print("║          2. Log In                 ║")
        print("║          3. Exit                   ║")
        print("╚════════════════════════════════════╝")
        choice = input("Please select an option: ")
        match choice:
            case "1":
                create_account()
            case "2":
                user = login()
                if user:
                    menu(user)
            case "3":
                save_accounts()
                exit("Thank you for your preference! Come back anytime!")
            case _:
                print("Invalid input. Please try again.")


def menu(acc: Account, filename: str = "accounts.json") -> None:
    while True:
        print("╔════════════════════════════════════╗")
        print("║        1. Deposit                  ║")
        print("║        2. Withdrawal               ║")
        print("║        3. Transfer                 ║")
        print("║        4. Check Balance            ║")
        print("║        5. Get Statement            ║")
        print("║        6. Log Out                  ║")
        print("╚════════════════════════════════════╝")
        choice = input("Please select an option: ")
        match choice:
            case "1":
                value = float(input("Value to deposit: "))
                acc.deposit(value)
                save_account(acc, filename)
            case "2":
                value = float(input("Value to withdrawal: "))
                acc.withdrawal(value)
                save_account(acc, filename)
            case "3":
                dest_acc_number = int(input("Destination account number: "))
                dest = get_account_by_id(dest_acc_number)
                if dest:
                    value = float(input("Value to transfer: "))
                    acc.transfer(dest, value)
                    save_account(acc, filename)
                    save_account(dest, filename)
                else:
                    print("Invalid destination account.")
            case "4":
                print(f"Balance: {format_float_to_currency_str(acc.balance)}")
            case "5":
                acc.get_statement()
            case "6":
                save_account(acc, filename)
                return


def check_existing_cpf(cpf: str, filename: str) -> bool:
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == cpf:
                    return True
    except FileNotFoundError:
        pass
    return False


def check_existing_username(username: str, filename: str) -> bool:
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == username:
                    return True
    except FileNotFoundError:
        pass
    return False


def create_account(csv_filename: str = "usernames.csv", json_filename: str = "accounts.json") -> None:
    global accounts
    print("First, we need some information about you.")
    name = input("Name: ")
    cpf = input("CPF: ")

    if check_existing_cpf(cpf, csv_filename):
        print("CPF already exists. Unable to create account.")
    else:
        print("Now, we need an username and password for you to access your account.")
        username = input("Username: ")
        while check_existing_username(username, csv_filename):
            print("Username already exists. Please insert another one.")
            username = input("Username: ")
        psswd = get_password()

        new_client = Client(name, cpf)
        new_account = Account(new_client)
        save_account(new_account, json_filename)

        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(["cpf", "username", "password"])
            writer.writerow([cpf, username, psswd])

        print("Account created successfully.")
                

def get_account_by_cpf(cpf: str) -> Union[Account, None]:
    for account in accounts.values():
        if account.client.cpf == cpf:
            return account
    return None


def get_account_by_id(id: int) -> Union[Account, None]:
    return accounts.get(id, None)


def get_password():
    return getpass.getpass("Password: ")


def login(filename: str = "usernames.csv") -> Union[Account, None]:
    username = input("Username: ")
    if check_existing_username(username, filename):
        psswd = get_password()
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == username:
                    if row[2] == psswd:
                        cpf = row[0]
                        return get_account_by_cpf(cpf)
                    else:
                        print("Incorrect password.")
                        return None
    else:
        print("This username doesn't exist.")
    return None


def load_accounts(filename: str = "accounts.json"):
    global accounts
    try:
        with open(filename, mode='r') as file:
            accounts_data = json.load(file)
            for acc_number, acc_data in accounts_data.items():
                account = Account.from_dict(acc_data)
                accounts[acc_number] = account
    except FileNotFoundError:
        pass


def save_accounts(filename: str = "accounts.json") -> None:
    accounts_data = {account.number: account.to_dict() for account in accounts.values()}
    with open(filename, mode="w") as file:
        json.dump(accounts_data, file, indent=4)


def save_account(account: Account, filename: str = "accounts.json") -> None:
    accounts[account.number] = account
    save_accounts(filename)


if __name__ == "__main__":
    main()
