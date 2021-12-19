import os
import django
import requests
import json
import yahoo_fin.stock_info as si

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finalproject.settings')
django.setup()

from trade.models import Stock

def get_stocks():
    tickers = si.tickers_sp500()
    for ticker in tickers:
        data = si.get_live_price(ticker)
        stock, created = Stock.objects.get_or_create(name = ticker, defaults = {'price': data})
        if not created:
            print(f'updated old stock {stock.name}')
            stock.price = data
            stock.save()
        else:
            print(f'created new stock {stock.name}')
    return Stock.objects.all()

stocks = get_stocks()

    



