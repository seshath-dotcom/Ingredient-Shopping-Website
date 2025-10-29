from django.db import models
import os
from ckeditor.fields import RichTextField
# Create your models here.

def filepath(request, filename):
    """ old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename) """
    return os.path.join('image/', filename)

class Dish(models.Model):
    title = models.TextField()
    image = models.ImageField(upload_to=filepath)
    description = models.TextField()
    ingredients_detail = models.TextField(blank=True, null=True)
    ingredients = models.ManyToManyField("Ingredients")
    cook_time = models.CharField(max_length=250)
    prep_time = models.CharField(max_length=250)
    servings = models.IntegerField()
    intructions = models.TextField()
    nutritional_facts = RichTextField(blank=True, null=True)
    created_on =  models.DateTimeField(auto_now_add=True)
    updated_on =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class meta:
        db_table = 'dish'   

class Ingredients(models.Model):
    name = models.TextField()
    image = models.ImageField(upload_to=filepath)
    description = models.TextField()
    quantity = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return self.name
    
    class meta:
        db_table = 'ingredients'

