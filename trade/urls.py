from django.urls import path
from . import views


urlpatterns = [
    path('homepage/', views.AvailableSalesListView.as_view(), name='homepage'),
    path('sell/<int:pk>/', views.SaleDetailView.as_view(), name='sell'),
    path('newsale/<int:stock_pk>/',
         views.SaleCreateView.as_view(), name='newsale'),
    path('offer/<int:sell_pk>/',
         views.OfferCreateView.as_view(), name='offer'),
    path('handleoffer/<int:buy_pk>/<str:status>/',
         views.HandleOfferView.as_view(), name='handleoffer')
]