from django.db import models
from django.contrib.auth.models import User
import random

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portfolio = models.ManyToManyField('trade.Stock')
    money= models.IntegerField(default=0)
    completed_signup = models.BooleanField(default = False)

    def deal_cards(self):
        stock = self.__class__.portfolio.field.related_model.objects.all()
        random_stocks = random.sample(list(stock), 10)
        self.portfolio.add(*random_stocks)
    
    def sales_with_offers(self):
        return self.sell_set.filter(is_completed=False)
