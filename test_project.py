from client import Client
from account import Account
import project

import pytest
import os
import json
import csv


@pytest.fixture(autouse=True)
def setup():
    """Fixture to clean up test environment"""
    project.accounts.clear()
    yield
    if os.path.exists("test_usernames.csv"):
        os.remove("test_usernames.csv")
    if os.path.exists("test_accounts.json"):
        os.remove("test_accounts.json")


def _create_account(monkeypatch):
    """Helper method to simulate user input and create an account"""
    inputs = iter(["Test User", "12345678900", "testuser", "password"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('project.get_password', lambda: next(inputs))
    project.create_account("test_usernames.csv", "test_accounts.json")


def test_create_account(monkeypatch):
    _create_account(monkeypatch)

    # Check if the object Account was created correctly:
    assert len(project.accounts) == 1
    account = list(project.accounts.values())[0]
    assert account.client.name == "Test User"
    assert account.client.cpf == "12345678900"

    # Check if the data was saved correctly in the CSV file:
    with open("test_usernames.csv", mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        assert len(rows) == 2   # Header + 1 row
        assert rows[1] == ["12345678900", "testuser", "password"]

    # Check if the data was saved correctly in the JSON file:
    with open("test_accounts.json", mode='r') as file:
        accounts_data = json.load(file)
        assert len(accounts_data) == 1
        acc_number = list(accounts_data.keys())[0]
        assert accounts_data[acc_number]["client"]["name"] == "Test User"
        assert accounts_data[acc_number]["client"]["cpf"] == "12345678900"


# Running a test multiple times with different sets of parameters.
@pytest.mark.parametrize("username, password, expected", [
    ("testuser", "password", True),         # Correct credentials
    ("testuser", "wrongpassword", False),   # Incorrect password
    ("nonexistentuser", "password", False)  # Non-existent user
])
def test_login(monkeypatch, username, password, expected):
    _create_account(monkeypatch)

    # Simulate user input for login:
    inputs = iter([username, password])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    monkeypatch.setattr('project.get_password', lambda: next(inputs))

    logged_in_account = project.login("test_usernames.csv")

    # Check if login was sucessful or failed as expected:
    if expected:
        assert logged_in_account is not None
        assert logged_in_account.client.name == "Test User"
        assert logged_in_account.client.cpf == "12345678900"
    else:
        assert logged_in_account is None


def test_deposit():
    client = Client("Test User", "12345678900")
    account = Account(client)
    account.deposit(100.0)

    assert account.balance == 100.0


def test_withdrawal():
    client = Client("Test User", "12345678900")
    account = Account(client)
    account.deposit(100.0)
    account.withdrawal(50.0)

    assert account.balance == 50.0


def test_transfer():
    client1 = Client("User One", "12345678900")
    account1 = Account(client1)
    client2 = Client("User Two", "09876543211")
    account2 = Account(client2)
    account1.deposit(100.0)
    account1.transfer(account2, 50.0)

    assert account1.balance == 50.0
    assert account2.balance == 50.0


def test_get_statement():
    client = Client("Test User", "12345678900")
    account = Account(client)
    account.deposit(100.0)
    account.withdrawal(50.0)
    statement = account.statement

    assert statement[0]['Type'] == "Deposit"
    assert statement[0]['Value'] == "R$ 100.00"
    assert statement[1]['Type'] == "Withdrawal"
    assert statement[1]['Value'] == "R$ 50.00"


def test_save_accounts():
    client = Client("Test User", "12345678900")
    account = Account(client)
    account.deposit(100.0)
    account.withdrawal(50.0)
    project.save_account(account, "test_accounts.json")

    # Check if the data was saved correctly in the JSON file:
    with open("test_accounts.json", mode='r') as file:
        accounts_data = json.load(file)
        assert len(accounts_data) == 1
        acc_number = list(accounts_data.keys())[0]

        assert accounts_data[acc_number]["balance"] == 50.0
        assert accounts_data[acc_number]["statement"][0]['Type'] == "Deposit"
        assert accounts_data[acc_number]["statement"][0]['Value'] == "R$ 100.00"
        assert accounts_data[acc_number]["statement"][1]['Type'] == "Withdrawal"
        assert accounts_data[acc_number]["statement"][1]['Value'] == "R$ 50.00"
