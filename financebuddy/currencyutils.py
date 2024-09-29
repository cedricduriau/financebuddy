# third party
import babel.numbers
import pycountry


def validate_currency(currency: str) -> str:
    code = pycountry.currencies.get(alpha_3=currency)
    if code is None:
        raise ValueError(f"unknown currency: {currency}")
    return code.alpha_3


def get_currency_precision(currency: str) -> int:
    format_str = babel.numbers.format_currency(1, currency, locale="en_US", format="#,##0.00")

    parts = format_str.split(".")
    try:
        _, digits = parts
    except ValueError:
        digits = ""

    precision = len(digits)
    return precision


def calculate_smallest_value(value: int | float, currency: str) -> int:
    precision = get_currency_precision(currency)
    smallest_value = int(value * (10**precision))
    return smallest_value


def calculate_currency_value(value: int, currency: str) -> float:
    precision = get_currency_precision(currency)
    currency_value = float(value / (10**precision))
    return currency_value


def format_value(value: int, currency: str) -> str:
    precision = get_currency_precision(currency)
    display_value = value / (10**precision)
    formatted = babel.numbers.format_currency(display_value, currency, locale="en_US", format="#,##0.00")
    return formatted


def list_currencies() -> list[str]:
    currencies = list(babel.numbers.list_currencies())
    currencies.sort()
    return currencies
