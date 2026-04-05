import requests
from django.core.management.base import BaseCommand
from portfolio.models import Price, Asset
class Command(BaseCommand):
    help = "Mark top 1000 cryptocurrencies"

    def handle(self, *args, **kwargs):
        price_to_update = []
        price_to_create = []

        response = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params={
                "vs_currency": "rub",
                "order": "market_cap_desc",
                "per_page": 250,
                "page": 1
                }
            )
        data = response.json()

        ids = []  #Создание массива с external_id
        for item in data:
            ids.append(item["id"])
        assets = Asset.objects.filter(external_id__in=ids)
        assets_mapping = {} #Создание меппинга(external_id -> asset) для того, чтобы делать только 1 запрос к бд
        for asset in assets:
            assets_mapping[asset.external_id] = asset
        prices = Price.objects.filter(asset__in=assets)
        prices_mapping = {} #Создание меппинга(asset.id -> price) для того, чтобы делать только 1 запрос к бд
        for price in prices:
            prices_mapping[price.asset_id] = price

        for item in data:
            asset = assets_mapping.get(item["id"])
            if not asset:
                continue
            price = prices_mapping.get(asset.id)
            if price: #Если топ изменился и для asset нет таблицы price, то нужно создать её, если нет - обновить данные
                price.price = item["current_price"]
                price.market_cap = item["market_cap"]
                price_to_update.append(price)
            else:
                price_to_create.append(
                    Price(
                        asset=asset,
                        price=item["current_price"],
                        market_cap=item["market_cap"],
                    )
                )
        Price.objects.bulk_update(price_to_update, ["price", "market_cap"])
        if price_to_create:
            Price.objects.bulk_create(price_to_create)
        self.stdout.write(self.style.SUCCESS("Price updated successfully"))