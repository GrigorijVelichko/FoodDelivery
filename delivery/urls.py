from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('', views.RestaurantListView.as_view(), name='restaurant_list'),
    path('restaurant/<int:pk>/', views.RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('cart/', views.CartDetailView.as_view(), name='cart_detail'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
]