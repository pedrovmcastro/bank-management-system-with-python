from datetime import date, datetime


def date_to_str(data: date) -> str:
    return data.strftime("%Y/%m/%d")


def time_to_str(time: datetime) -> str:
    return time.strftime("%H:%M")


def str_to_date(data: str) -> date:
    return datetime.strptime(data, "%Y/%m/%d")


def format_float_to_currency_str(value: float) -> str:
    return f"R$ {value:,.2f}"
