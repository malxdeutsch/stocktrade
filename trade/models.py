from django.db import models

# Create your models here.

class Stock(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=200)

    def rarity(self):
        if self.position == 'P':
            return 5
        else:
            return 0

    def __str__(self):
        return self.name


class Sell (models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    profile = models.ForeignKey('account.Profile', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def viable_offers(self):
        return self.buy_set.filter(is_rejected=False)


class Buy (models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, blank=True)
    profile = models.ForeignKey('account.Profile', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    sell = models.ForeignKey(Sell, on_delete=models.CASCADE)
    is_rejected = models.BooleanField(default=False)

    def accept(self):
        if not self.sell.is_completed:
            self.sell.profile.portfolio.remove(self.sell.stock)
            self.profile.portfolio.add(self.sell.stock)
            self.sell.profile.portfolio.add(self.stock)
            self.profile.portfolio.remove(self.stock)
            self.sell.profile.money -= float(self.sell.stock.price)
            self.profile.money += float(self.sell.stock.price)
            self.sell.is_completed = True
            self.sell.save()
            self.sell.profile.save()
            self.profile.save()
            return True
        return False

    def reject(self):
        self.is_rejected = True
        self.save()