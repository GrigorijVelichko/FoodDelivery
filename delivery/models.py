from django.db import models

from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
  name = models.CharField(max_length=100, unique=True, verbose_name='Category')
  slug = models.SlugField(max_length=100, unique=True)

  class Meta:
    verbose_name = 'Category'
    verbose_name_plural = 'Categories'

  def __str__(self):
    return self.name


class Restaurant(models.Model):
  name = models.CharField(max_length=150, verbose_name='Restaurant Name')
  description = models.TextField(blank=True, verbose_name='Description')
  address = models.CharField(max_length=255, verbose_name='Address')
  phone = models.CharField(max_length=20, verbose_name='Phone')
  image = models.ImageField(
      upload_to='restaurants/', blank=True, null=True, verbose_name='Logo'
  )
  is_active = models.BooleanField(default=True, verbose_name='Is Active')

  class Meta:
    verbose_name = 'Restaurant'
    verbose_name_plural = 'Restaurants'

  def __str__(self):
    return self.name


class FoodItem(models.Model):
  restaurant = models.ForeignKey(
      Restaurant,
      on_delete=models.CASCADE,
      related_name='menu_items',
      verbose_name='Restaurant',
  )
  category = models.ForeignKey(
      Category,
      on_delete=models.SET_NULL,
      null=True,
      related_name='items',
      verbose_name='Category',
  )
  name = models.CharField(max_length=150, verbose_name='Dish Name')
  description = models.TextField(blank=True, verbose_name='Ingredients / Description')
  price = models.DecimalField(
      max_digits=8, decimal_places=2, verbose_name='Price'
  )
  image = models.ImageField(
      upload_to='food_items/', blank=True, null=True, verbose_name='Dish Image'
  )
  is_available = models.BooleanField(
      default=True, verbose_name='Is Available'
  )

  class Meta:
    verbose_name = 'Food Item'
    verbose_name_plural = 'Food Items'

  def __str__(self):
    return f'{self.name} ({self.restaurant.name})'


class Cart(models.Model):
  user = models.ForeignKey(
      User,
      on_delete=models.CASCADE,
      related_name='cart',
      verbose_name='User',
  )
  created_at = models.DateTimeField(
      auto_now_add=True, verbose_name='Created At'
  )

  class Meta:
    verbose_name = 'Cart'
    verbose_name_plural = 'Carts'

  def __str__(self):
    return f"Cart for user {self.user.username}"


class CartItem(models.Model):
  cart = models.ForeignKey(
      Cart,
      on_delete=models.CASCADE,
      related_name='items',
      verbose_name='Cart',
  )
  food_item = models.ForeignKey(
      FoodItem, on_delete=models.CASCADE, verbose_name='Food Item'
  )
  quantity = models.PositiveIntegerField(default=1, verbose_name='Quantity')

  class Meta:
    verbose_name = 'Cart Item'
    verbose_name_plural = 'Cart Items'

  def __str__(self):
    return f'{self.quantity} x {self.food_item.name}'

  @property
  def total_price(self):
    return self.food_item.price * self.quantity


class Order(models.Model):
  STATUS_CHOICES = [
      ('pending', 'Pending'),
      ('preparing', 'Preparing'),
      ('on_the_way', 'On the way'),
      ('delivered', 'Delivered'),
      ('cancelled', 'Cancelled'),
  ]

  user = models.ForeignKey(
      User,
      on_delete=models.CASCADE,
      related_name='orders',
      verbose_name='User',
  )
  restaurant = models.ForeignKey(
      Restaurant,
      on_delete=models.SET_NULL,
      null=True,
      verbose_name='Restaurant',
  )
  status = models.CharField(
      max_length=20,
      choices=STATUS_CHOICES,
      default='pending',
      verbose_name='Order Status',
  )
  shipping_address = models.CharField(
      max_length=255, verbose_name='Shipping Address'
  )
  phone = models.CharField(max_length=20, verbose_name='Phone')
  total_price = models.DecimalField(
      max_digits=10, decimal_places=2, verbose_name='Total Price'
  )
  created_at = models.DateTimeField(
      auto_now_add=True, verbose_name='Created At'
  )
  updated_at = models.DateTimeField(
      auto_now=True, verbose_name='Updated At'
  )

  class Meta:
    verbose_name = 'Order'
    verbose_name_plural = 'Orders'

  def __str__(self):
    return f'Order #{self.id} by {self.user.username}'


class OrderItem(models.Model):
  order = models.ForeignKey(
      Order,
      on_delete=models.CASCADE,
      related_name='items',
      verbose_name='Order',
  )
  food_item = models.ForeignKey(
      FoodItem, on_delete=models.SET_NULL, null=True, verbose_name='Food Item'
  )
  price = models.DecimalField(
      max_digits=8, decimal_places=2, verbose_name='Price at Order'
  )
  quantity = models.PositiveIntegerField(default=1, verbose_name='Quantity')

  class Meta:
    verbose_name = 'Order Item'
    verbose_name_plural = 'Order Items'

  def __str__(self):
    return f'{self.quantity} x {self.food_item.name if self.food_item else "Deleted"}'