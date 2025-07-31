import os
import requests

from dotenv import load_dotenv
load_dotenv()

EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")

def compare_exchange_rate(base_currency=None, target_currency=None, amount: float = 1.0):
    """
        base_currency: The currency to convert from (e.g., "USD").
        target_currency: The currency to convert to (e.g., "EUR").
        amount: The amount to convert (not used in this function, but can be used for future enhancements).
    """
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/pair/{base_currency}/{target_currency}/{amount}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    return None
