from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, RedirectView
from django.contrib.auth.models import User
from .models import Stock, Sell, Buy
from django.contrib import messages
from .forms import BuyForm
from .apiinteraction import high_gained_earnings

# Create your views here.

class AvailableSalesListView(ListView):
    model = Sell
    template_name = 'homepage.html'
    queryset = Sell.objects.filter(is_completed=False)
    
    def get_context_data(self, **kwargs):
        context=  super().get_context_data(**kwargs)
        context['gainers'] = high_gained_earnings()
        Stock.get_stocks()
        return context

class SaleDetailView(DetailView):
    model = Sell
    template_name = 'saledetails.html'
    queryset = Sell.objects.filter(is_completed=False)


class SaleCreateView(RedirectView):
    pattern_name = 'homepage'

    def get_redirect_url(self, *args, **kwargs):
        stock = Stock.objects.get(id=self.kwargs['stock_pk'])
        if stock in self.request.user.profile.portfolio.all():
            sell, created = Sell.objects.get_or_create(
                stock= stock, profile=self.request.user.profile, is_completed=False)
            if created:
                messages.success(
                    self.request, f'Successful sale offer for {stock.name}!')
            else:
                messages.warning(
                    self.request, f'This card is currently being offered for sale.')
        else:
            messages.error(self.request, 'You can\'t sell others\' cards')
        return super().get_redirect_url()


class OfferCreateView(CreateView):
    form_class = BuyForm
    template_name = 'offerpurchase.html'

    def get_success_url(self):
        return reverse_lazy('sell', kwargs={'pk': self.object.sell.id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        buy = form.save(commit=False)
        buy.profile = self.request.user.profile
        buy.sell_id = self.kwargs['sell_pk']
        buy.save()
        if buy.is_purchase:
            buy.accept()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        sell = get_object_or_404(Sell, id=self.kwargs['sell_pk'])
        if sell.profile == self.request.user.profile:
            messages.error(
                self.request, 'You can\'t make an offer on your own trade.')
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)


class HandleOfferView(RedirectView):
    pattern_name = 'myprofile'
    def get_redirect_url(self, *args, **kwargs):
        buy = get_object_or_404(Buy, id=self.kwargs['buy_pk'])
        if self.request.user == buy.sell.profile.user:
            if self.kwargs['status'] == 'accept':
                if buy.accept():
                    messages.success(
                        self.request, 'Offer accepted successfully')
                else:
                    messages.warning(
                        self.request, 'Sale was already completed.')
            else:
                buy.reject()
                messages.success(self.request, 'Offer rejected successfully')
        else:
            messages.warning(
                self.request, 'You can\'t accept offers for other folks.')

        kwargs.clear()
        return super().get_redirect_url(*args, **kwargs)

