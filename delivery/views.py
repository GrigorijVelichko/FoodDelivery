from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
import models


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

class RestaurantListView(ListView):
    model = models.Restaurant
    template_name = "deliver/restaurant_list.html"
    context_object_name = "restaurants"

    def get_queryset(self):
        return models.Restaurant.objects.filter(is_active=True)

class RestaurantDetailView(DetailView):
    model = models.Restaurant
    template_name = "deliver/restaurant_detail.html"
    context_object_name = "restaurant"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["food_items"] = self.object.menu_items.filter(is_available=True)
        return context

class CartDetailView(DetailView):
    model = models.Cart
    template_name = "deliver/cart_detail.html"
    context_object_name = "cart"

class OrderListView(ListView):
    model = models.Order
    template_name = "deliver/order_list.html"
    context_object_name = "orders"

    def get_queryset(self, Order):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')