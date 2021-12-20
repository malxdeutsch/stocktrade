from django import forms
from django.forms import ModelForm
from .models import Stock, Sell, Buy

class BuyForm(forms.ModelForm):
    class Meta:
        model = Buy
        fields = ['stock']



    def __init__(self, user, *args, **kwargs):
        super(BuyForm, self).__init__(*args, **kwargs)
        self.fields['stock'].queryset= user.profile.portfolio.all()