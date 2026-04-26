import requests
from portfolio.models import Asset, Price
from django.core.management.base import BaseCommand
from django.db import transaction
from .import_rus_assets import get_moex_assets

class Command(BaseCommand):
    help = 'Update RUS assets'
    def handle(self, *args, **options):
        assets_data = get_moex_assets()

        tickers = [item["ticker"] for item in assets_data]

        assets_map = {
            asset.external_id: asset
            for asset in Asset.objects.filter(external_id__in=tickers)
        }

        prices_map = {
            price.asset_id: price
            for price in Price.objects.filter(asset__external_id__in=tickers)
        }

        prices_to_update = []

        for item in assets_data:
            asset = assets_map.get(item["ticker"])

            if not asset:
                continue

            price_obj = prices_map.get(asset.id)

            if not price_obj:
                continue

            price_obj.price = item["price"]
            prices_to_update.append(price_obj)

        with transaction.atomic():
            Price.objects.bulk_update(
                prices_to_update,
                ["price"],
                batch_size=500,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Обновлено цен: {len(prices_to_update)}"
            )
        )
