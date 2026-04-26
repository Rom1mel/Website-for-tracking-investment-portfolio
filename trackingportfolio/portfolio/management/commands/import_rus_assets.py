import requests
from portfolio.models import Asset, Price
from django.core.management.base import BaseCommand
from django.db import transaction


def table_to_dicts(table):
    columns = table["columns"]
    return [dict(zip(columns, row)) for row in table["data"]]


def get_moex_assets():
    url = "https://iss.moex.com/iss/engines/stock/markets/shares/securities.json"

    params = {
        "iss.meta": "off",
        "iss.only": "securities,marketdata",
        "securities.columns": "SECID,BOARDID,SHORTNAME,SECNAME",
        "marketdata.columns": "SECID,BOARDID,LAST,MARKETPRICE,LCURRENTPRICE,BID,OFFER,SYSTIME",
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()

    securities = table_to_dicts(data["securities"])
    marketdata = table_to_dicts(data["marketdata"])

    names = {
        (row["SECID"], row["BOARDID"]): {
            "shortname": row.get("SHORTNAME"),
            "name": row.get("SECNAME"),
        }
        for row in securities
    }

    result = []

    for row in marketdata:
        price = (
            row.get("LAST")
            or row.get("MARKETPRICE")
            or row.get("LCURRENTPRICE")
            or row.get("BID")
            or row.get("OFFER")
        )

        if not price:
            continue

        key = (row["SECID"], row["BOARDID"])
        name_info = names.get(key, {})

        result.append({
            "ticker": row["SECID"],
            "board": row["BOARDID"],
            "shortname": name_info.get("shortname"),
            "name": name_info.get("name"),
            "price": price,
            "price_time": row.get("SYSTIME"),
        })

    return result

class Command(BaseCommand):
    help = "Import MOEX assets"

    def handle(self, *args, **options):
        assets = get_moex_assets()

        unique_assets = {}

        for item in assets:
            ticker = item["ticker"]

            if ticker not in unique_assets:
                unique_assets[ticker] = item

        assets = list(unique_assets.values())

        self.stdout.write(f"Получено уникальных активов: {len(assets)}")

        asset_objects = []

        for asset in assets:
            asset_objects.append(
                Asset(
                    ticker=asset["ticker"],
                    name=asset["name"] or asset["shortname"],
                    type="stock_rus",
                    external_id=asset["ticker"],
                )
            )

        Asset.objects.bulk_create(
            asset_objects,
            ignore_conflicts=True,
            batch_size=500,
        )

        tickers = [asset["ticker"] for asset in assets]

        assets_map = {
            asset.external_id: asset
            for asset in Asset.objects.filter(external_id__in=tickers)
        }

        existing_price_asset_ids = set(
            Price.objects.filter(
                asset__external_id__in=tickers
            ).values_list("asset_id", flat=True)
        )

        price_objects = []

        for item in assets:
            asset = assets_map.get(item["ticker"])

            if not asset:
                continue

            if asset.id in existing_price_asset_ids:
                continue

            price_objects.append(
                Price(
                    asset=asset,
                    price=item["price"],
                )
            )

        Price.objects.bulk_create(
            price_objects,
            batch_size=500,
        )

        self.stdout.write(
            self.style.SUCCESS(f"Создано цен: {len(price_objects)}")
        )