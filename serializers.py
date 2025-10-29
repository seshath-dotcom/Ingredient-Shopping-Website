from .models import Dish, Ingredients
from rest_framework import serializers




class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = "__all__"

class DishSerializer(serializers.ModelSerializer): 
    ingredients = IngredientsSerializer(many=True)
    class Meta: 
        model = Dish 
        fields = "__all__"

class DishSearchSerializer(serializers.ModelSerializer): 

    class Meta: 
        model = Dish 
        fields = ('title','id')