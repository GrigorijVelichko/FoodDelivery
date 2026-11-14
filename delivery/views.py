from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = "deliver/login.html"
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = "deliver:login"

class RegisterView(CreateView):
    template_name = "deliver/register.html"
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse_lazy("deliver:login"))
