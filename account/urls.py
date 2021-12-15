from django.urls import path
from .views import SignupView, ProfileDetailView, MyProfileDetailView, MyProfileUpdateView
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('profile/', MyProfileDetailView.as_view(), name='myprofile'),
    path('completesignup/', MyProfileUpdateView.as_view(), name='complete'),
]
