from datetime import date
from helper import date_to_str

class Client:

    counter: int = 101
    
    def __init__(self, name: str, cpf: str) -> None:
        self.__id: int = Client.counter
        self.__cpf: str = cpf
        self.__name: str = name
        self.__registration_date: date = date.today()
        Client.counter += 1

    @property
    def id(self) -> int:
        return self.__id

    @property
    def cpf(self) -> str:
        return self.__cpf

    @property
    def name(self) -> str:
        return self.__name

    @property
    def registration_date(self) -> int:
        return date_to_str(self.__registration_date)
    
    def __str__(self) -> str:
        return f"Client ID: {self.id}\nName: {self.name}\nRegistration Date: {self.registration_date}\n"
    