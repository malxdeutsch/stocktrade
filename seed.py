import os
import django
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finalproject.settings')
django.setup()

from trade.models import Stock

stocks = Stock.get_stocks()

    



