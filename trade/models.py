from django.db import models
import yahoo_fin.stock_info as si
from datetime import timedelta
from django.utils import timezone

# Create your models here.

class Stock(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    last_updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

    @classmethod
    def get_stocks(cls):
        if cls.objects.all().exists():
            if timezone.now() - cls.objects.first().last_updated < timedelta(minutes= 20):
                return
        tickers = si.tickers_sp500()
        for ticker in tickers:
            data = si.get_live_price(ticker)
            stock, created = cls.objects.get_or_create(name = ticker, defaults = {'price': data})
            if not created:
                print(f'updated old stock {stock.name}')
                stock.price = data
                stock.save()
            else:
                print(f'created new stock {stock.name}')
        return cls.objects.all()

class Sell (models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    profile = models.ForeignKey('account.Profile', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def viable_offers(self):
        return self.buy_set.filter(is_rejected=False)


class Buy (models.Model):
    stock = models.ManyToManyField(Stock, blank=True)
    profile = models.ForeignKey('account.Profile', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    sell = models.ForeignKey(Sell, on_delete=models.CASCADE)
    is_rejected = models.BooleanField(default=False)

    @property
    def is_purchase(self):
        return not self.stock.all().exists()


    def accept(self):
        if not self.sell.is_completed:
            self.sell.profile.portfolio.remove(self.sell.stock)
            self.profile.portfolio.add(self.sell.stock)
            self.sell.profile.portfolio.add(*self.stock.all())
            self.profile.portfolio.remove(*self.stock.all())
            if self.is_purchase:
                self.sell.profile.money -= float(self.sell.stock.price)
                self.profile.money += float(self.sell.stock.price)
                self.sell.profile.save()
                self.profile.save()
            self.sell.is_completed = True
            self.sell.save()
            return True
        return False

    def reject(self):
        self.is_rejected = True
        self.save()