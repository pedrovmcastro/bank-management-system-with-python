from datetime import date, datetime
from client import Client
from helper import format_float_to_currency_str, date_to_str, time_to_str, str_to_date

class Account:

    code: int = 1001

    def __init__(self, client: Client, balance: float = 0.0, number: int = None, statement: list = None) -> None:
        self.__number: int = number if number else Account.code
        self.__client: Client = client
        self.__balance: float = balance
        self.__statement: list = statement if statement else []
        self.__creation_date: date = date.today()
        Account.code += 1

    def __str__(self) -> str:
        return f"Account number: {self.number}\nClient: {self.client.name}\
            \nBalance: {format_float_to_currency_str(self.balance)}\n"
        
    @property
    def number(self) -> int:
        return self.__number
    
    @property 
    def client(self) -> Client:
        return self.__client
    
    @property
    def balance(self) -> float:
        return self.__balance
    
    @balance.setter
    def balance(self, value: float):
        self.__balance: float = value
    
    @property
    def statement(self) -> list:
        return self.__statement
    
    @statement.setter
    def statement(self, statement: list):
        self.__statement: list = statement
    
    @property
    def creation_date(self) -> date:
        return self.__creation_date
    
    
    def deposit(self, value: float) -> None:
        try:
            if value > 0:
                self.balance += value
                self.__update_statement("Deposit", value)               
                print("Deposit successful!")
            else:
                raise ValueError("Invalid value.")
        except (ValueError, TypeError) as err:
            print(err)
            
      
    def withdrawal(self, value: float) -> None:
        try:
            if value > 0:
                if self.balance >= value:
                    self.balance -= value
                    self.__update_statement("Withdrawal", value) 
                    print("Withdrawal successful!")
                else:
                    raise ValueError("Insufficient funds.")
            else:
                raise ValueError("Invalid value.")
        except (ValueError, TypeError) as err:
            print(err)


    def transfer(self, dest: object, value: float) -> None:
        try:
            if not isinstance(dest, Account) or dest.number == self.number:
                raise ValueError("Invalid destination account.")
            if value > 0:
                if self.balance >= value:
                    self.balance -= value
                    dest.balance += value
                    self.__update_statement("Transfer", value, destination=dest.client.name)
                    dest.__update_statement("Transfer", value, origin=self.client.name)
                    print("Transfer completed successfully!")
                else:
                    raise ValueError("Insufficient funds.")
            else:
                raise ValueError("Invalid value.")
        except (ValueError, TypeError) as err:
            print(err)
            print("Transfer not completed. Try again.")

    
    def __update_statement(self, transaction_type: str, value: float, destination: str = None, origin: str = None) -> None:
        transaction = {
            "Type": transaction_type,
            "Value": format_float_to_currency_str(value),
            "Date": date_to_str(date.today()),
            "Time": time_to_str(datetime.now()),
            "Balance": format_float_to_currency_str(self.balance)
        }
        if destination:
            transaction["Destination"] = destination
        if origin:
            transaction["Origin"] = origin
        self.statement.append(transaction)
        
    
    def get_statement(self) -> None:
        print(f"Statement for Account Number: {self.number}\n")
        print("Type         | Value           | Date       |  Time | Balance")
        print("-" * 65)
        for transaction in self.statement:
            destination = transaction.get("Destination")
            origin = transaction.get("Origin")
            if destination:
                print(f"{transaction['Type']:12} | {transaction['Value']:15} | {transaction['Date']} | {transaction['Time']} | {transaction['Balance']}  To: {transaction['Destination']}")
            elif origin:
                print(f"{transaction['Type']:12} | {transaction['Value']:15} | {transaction['Date']} | {transaction['Time']} | {transaction['Balance']}  From: {transaction['Origin']}")
            else:
                print(f"{transaction['Type']:12} | {transaction['Value']:15} | {transaction['Date']} | {transaction['Time']} | {transaction['Balance']}")
        print()
        
    
    def to_dict(self) -> dict:
        return {
            "number": self.number,
            "client": {
                "name": self.client.name,
                "cpf": self.client.cpf,
            },
            "balance": self.balance,
            "creation_date": date_to_str(self.creation_date),
            "statement": self.statement
        }
    

    @classmethod
    def from_dict(cls, data):
        client_data = data["client"]
        client = Client(client_data["name"], client_data["cpf"])
        account = cls(client, number=data["number"], balance=data["balance"])
        account.statement = data.get("statement", [])
        return account
