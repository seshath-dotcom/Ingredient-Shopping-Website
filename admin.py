from django.contrib import admin
from dish.models import Dish, Ingredients 

# Register your models here.

admin.site.register(Dish)
admin.site.register(Ingredients)