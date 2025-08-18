import os
"""
Abstract base class defining the interface for exchange rate services.

This class provides a common interface for various implementations 
of exchange rate services that can retrieve conversion rates between
different currencies for specific dates.

Implementations of this class should handle the actual API calls,
data lookups, or other mechanisms to obtain the exchange rates.
"""
import requests
import time
from datetime import date
from abc import ABC, abstractmethod

class ExchangeRateService(ABC):
    @abstractmethod
    def get_rate(self, from_currency: str, to_currency: str, on_date: date) -> float:
        pass

class DefaultExchangeRateService(ExchangeRateService):
    def get_rate(self, from_currency: str, to_currency: str, on_date: date) -> float:
        access_key = os.getenv("EXCHANGE_RATE_HOST_API_ACCESS_KEY")
        if not access_key:
            raise ValueError("Missing EXCHANGE_RATE_HOST_API_ACCESS_KEY environment variable")

        time.sleep(1)  # Sleep to avoid hitting API rate limits
        
        url = "https://api.exchangerate.host/historical"
        resp = requests.get(url, params={
            "date": on_date.isoformat(),
            "source": from_currency, 
            "currencies": to_currency, 
            "access_key": access_key})
        resp.raise_for_status()
        return resp.json()["quotes"][f"{from_currency}{to_currency}"]

class LocalExchangeRateService(ExchangeRateService):
    def get_rate(self, from_currency: str, to_currency: str, on_date: date) -> float:
        # Return a fixed mock rate for dry run mode
        print(f"[DRY RUN] Using mock exchange rate for {from_currency} to {to_currency} on {on_date}")
        return 0.25  # Example fixed rate for BRL to AUD