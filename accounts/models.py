from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
import requests


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def convert_balance(self, currency_code):
        """
        Convert balance from USD to the given currency using live rates from exchangerate.host
        """
        url = f"https://api.exchangerate.host/latest?base=USD&symbols={currency_code}"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            rate = data["rates"].get(currency_code)
            if rate:
                return round(self.balance * Decimal(str(rate)), 2)
            else:
                return None
        except Exception:
            return None
