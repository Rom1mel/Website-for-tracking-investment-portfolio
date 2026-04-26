import requests
import time
from django.core.management.base import BaseCommand
from portfolio.models import Asset
class Command(BaseCommand):
    help = "Mark top 1000 cryptocurrencies"

    def handle(self, *args, **kwargs):
        top_ids = []

        response = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
                params={
                    "vs_currency": "usd",
                    "order": "market_cap_desc",
                    "per_page": 250,
                    "page": 1
                }
            )

        if response.status_code != 200:
            print(f"Ошибка API: {response.status_code}")

        data = response.json()

        if not isinstance(data, list):
            print("API вернул не список:", data)

        for coin in data:
            top_ids.append(coin["id"])
        time.sleep(2)

        Asset.objects.filter(external_id__in=top_ids).update(type='top_crypto')