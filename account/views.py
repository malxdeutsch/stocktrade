from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic.base import RedirectView, TemplateView
from .forms import RegistrationForm, ProfileCreateForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import login, authenticate
# Create your views here.


class SignupView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('complete')
    template_name = 'signup.html'
    def form_valid(self, form):
        url = super().form_valid(form)
        user = authenticate(self.request, username = self.object.username, password = form.cleaned_data['password1'])
        if user:
            login(self.request, user)
        return url


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiledetail.html'

class MyProfileDetailView(ProfileDetailView):
    def get_object(self, queryset = None):
        return self.request.user.profile

class MyProfileUpdateView(UpdateView):
    model = Profile
    template_name = 'signup.html'
    fields = ['money']
    success_url = reverse_lazy('myprofile')

    def get_object(self):
        profile = self.request.user.profile
        if profile.completed_signup:
            raise Http404('Signup has already been comepleted; you cannot visit this page.')
        
        return self.request.user.profile
    
    def form_valid(self, form):
        self.request.user.profile.completed_signup = True
        self.request.user.profile.save()
        return super().form_valid(form)
