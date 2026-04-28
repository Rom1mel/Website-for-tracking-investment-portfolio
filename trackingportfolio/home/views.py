from collections import defaultdict

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from deals.models import Deal, Receipt
from portfolio.models import Portfolio, PortfolioAsset, Price


def _map_asset_type(asset_type):
    asset_type = (asset_type or "").lower()

    if "crypto" in asset_type:
        return "Криптовалюты"
    if "stock" in asset_type:
        return "Акции"
    if "etf" in asset_type:
        return "ETF"
    if "raw" in asset_type:
        return "Сырьё"
    return "Другое"


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")

    portfolios = list(Portfolio.objects.filter(user=request.user).order_by("name"))
    portfolio_ids = [portfolio.id for portfolio in portfolios]

    portfolio_assets = list(
        PortfolioAsset.objects.filter(portfolio__user=request.user).select_related("portfolio", "asset")
    )
    asset_ids = {portfolio_asset.asset_id for portfolio_asset in portfolio_assets}
    price_map = {
        price.asset_id: price.price
        for price in Price.objects.filter(asset_id__in=asset_ids)
    }

    portfolio_current_values = defaultdict(float)
    allocation_values = defaultdict(float)

    for portfolio_asset in portfolio_assets:
        current_price = price_map.get(portfolio_asset.asset_id, 0) or 0
        current_value = portfolio_asset.count * current_price

        portfolio_current_values[portfolio_asset.portfolio_id] += current_value
        allocation_values[_map_asset_type(portfolio_asset.asset.type)] += current_value

    receipts = list(Receipt.objects.filter(portfolio__user=request.user))
    net_invested_map = defaultdict(float)

    for receipt in receipts:
        if receipt.type == Receipt.ADD:
            net_invested_map[receipt.portfolio_id] += receipt.value
        elif receipt.type == Receipt.WITHDRAW:
            net_invested_map[receipt.portfolio_id] -= receipt.value

    total_balance = sum(portfolio.balance for portfolio in portfolios)
    total_asset_value = sum(portfolio_current_values.values())
    total_value = total_balance + total_asset_value

    top_portfolios = []
    total_net_invested = 0

    for portfolio in portfolios:
        current_assets_value = portfolio_current_values.get(portfolio.id, 0)
        current_volume = portfolio.balance + current_assets_value
        net_invested = net_invested_map.get(portfolio.id, 0)
        profit = current_volume - net_invested
        profitability = (profit / net_invested * 100) if net_invested > 0 else 0

        total_net_invested += net_invested

        top_portfolios.append(
            {
                "id": portfolio.id,
                "name": portfolio.name,
                "volume": current_volume,
                "profit": profit,
                "profitability": profitability,
            }
        )

    total_profit = total_value - total_net_invested
    total_profitability = (total_profit / total_net_invested * 100) if total_net_invested > 0 else 0
    portfolio_count = len(portfolios)

    recent_deals = list(
        Deal.objects.filter(portfolio__user=request.user)
        .select_related("asset", "portfolio")
        .order_by("-time_stamp")[:4]
    )

    allocation_total = sum(allocation_values.values())
    allocation_palette = {
        "Криптовалюты": "#20d489",
        "Акции": "#2f80ed",
        "ETF": "#7c4dff",
        "Сырьё": "#f8b51c",
        "Другое": "#27c0df",
    }

    allocation_data = []
    if allocation_total > 0:
        for label, value in sorted(allocation_values.items(), key=lambda item: item[1], reverse=True):
            percentage = value / allocation_total * 100
            allocation_data.append(
                {
                    "label": label,
                    "value": value,
                    "percentage": percentage,
                    "color": allocation_palette.get(label, "#27c0df"),
                }
            )

    allocation_chart = ""
    if allocation_data:
        current_point = 0
        chart_segments = []
        for item in allocation_data:
            next_point = current_point + item["percentage"]
            chart_segments.append(
                f"{item['color']} {current_point:.2f}% {next_point:.2f}%"
            )
            current_point = next_point
        allocation_chart = f"conic-gradient({', '.join(chart_segments)})"

    top_portfolios = sorted(
        top_portfolios,
        key=lambda portfolio: portfolio["profitability"],
        reverse=True,
    )[:4]

    stats = [
        {
            "label": "Общая стоимость",
            "value": total_value,
            "display": f"{total_value:.2f}",
            "suffix": "₽",
            "description": "Текущая стоимость всех портфелей",
            "accent": "neutral",
        },
        {
            "label": "Прибыль / Убыток",
            "value": total_profit,
            "display": f"{total_profit:.2f}",
            "suffix": "₽",
            "description": "С учётом активов, баланса и движений средств",
            "accent": "positive" if total_profit >= 0 else "negative",
        },
        {
            "label": "Доходность",
            "value": total_profitability,
            "display": f"{total_profitability:.2f}",
            "suffix": "%",
            "description": "Относительно чистых пополнений",
            "accent": "positive" if total_profitability >= 0 else "negative",
        },
        {
            "label": "Портфелей",
            "value": portfolio_count,
            "display": str(portfolio_count),
            "suffix": "",
            "description": "Активные портфели пользователя",
            "accent": "neutral",
        },
    ]

    context = {
        "stats": stats,
        "recent_deals": recent_deals,
        "allocation_data": allocation_data,
        "allocation_chart": allocation_chart,
        "has_allocation": bool(allocation_data),
        "top_portfolios": top_portfolios,
        "username": request.user.username,
    }
    return render(request, "home/Home.html", context)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})
