import requests
from django.core.management.base import BaseCommand
from portfolio.models import Asset


class Command(BaseCommand):
    help = "Import assets from CoinGecko"

    def handle(self, *args, **kwargs):
        url = "https://api.coingecko.com/api/v3/coins/list"

        response = requests.get(url)
        data = response.json()

        assets_to_create = []

        for item in data:
            assets_to_create.append(
                Asset(
                    name=item["name"],
                    ticker=item["symbol"],
                    type="crypto",
                    external_id=item["id"]
                )
            )

        Asset.objects.bulk_create(assets_to_create, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS("Assets imported successfully"))