import requests
from django.core.management.base import BaseCommand
from portfolio.models import Price, Asset
from django.db.models import Q

class Command(BaseCommand):
    help = "Обновляет цены непопулярных активов"
    def handle(self, *args, **options):
        assets = Asset.objects.filter(~Q(type__icontains='top'), asset__isnull=False).distinct()
        ids=[]
        for asset in assets:
            ids.append(asset.external_id)
        if not ids:
            self.stdout.write("Нет активов для обновления")
            return
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": ",".join(ids),
            "vs_currencies": "rub"
        }

        response = requests.get(url, params=params)
        data = response.json()

        updated = 0
        for asset in assets:
            if asset.external_id in data:
                price = data[asset.external_id]["rub"]
                Price.objects.update_or_create(
                    asset=asset,
                    defaults={"price": price}
                )
                updated += 1
        self.stdout.write(f"Обновлено цен: {updated}")