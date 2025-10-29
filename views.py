from django.shortcuts import render, redirect
from rest_framework import viewsets
from .serializers import DishSerializer, DishSearchSerializer, IngredientsSerializer
from .models import Dish, Ingredients
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse


@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)

class SignupView(View):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = '/receipe/dish'
    

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
    
    def post(self,request):
        form = UserCreationForm(request.POST)
            
        if form.is_valid():  
            form.save()
            return redirect('/login')
        

class LoginInterfaceView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    
    def get(self, request):  
        if request.user.is_authenticated:
            return redirect("/")
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
        
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            
            if user is not None:
                login(request, user)
                return redirect('/')
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})
    
class DishViewSet(viewsets.ModelViewSet):

    queryset = Dish.objects.all()
    serializer_class = DishSerializer

    
   
class IngredientsViewSet(viewsets.ModelViewSet):

    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer


def search(request):
    print(request.GET.get("name"))
    queryset =Dish.objects.filter(title__icontains=request.GET.get("name")).all()
    serializer =DishSearchSerializer(queryset, many=True)
    return JsonResponse({"data":serializer.data,"status":201})

def home(request):
    
    dish = Dish.objects.all()
    serializer =DishSerializer(dish,many=True)
    
    context ={
        "home_slider":list(serializer.data)[:8],
        "data":list(serializer.data)[:10]
    }
    return render(request,'index.html',context=context)

def recipe(request,id):
    dish = Dish.objects.get(pk=id)
    serializer =DishSerializer(dish,many=False)
    ingredients_detail =serializer.data['ingredients_detail'].split("\n")
    _ingredients =[]
    for ingredient in serializer.data['ingredients']:
        ig =list(filter(lambda x:ingredient['name'].lower() in x.lower(),ingredients_detail))
        if ig and ig[0]:
            _ingredients.append({
                "id":ingredient['id'],
                "name":ig[0]
            })
            return render(request,'receipe-post.html',context={"dish":serializer.data,"ingredients_detail":_ingredients})
# Create your views here.

def recipeall(request):
    dish = Dish.objects.all()
    serializer =DishSerializer(dish,many=True)
    context ={
        "data":list(serializer.data)
    }
    

    return render(request,'recipes.html',context=context)

@login_required(login_url="/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Ingredients.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")

@login_required(login_url="/login")
def cart_multiadd(request):
    if request.method =='POST':
        cart = Cart(request)
        for id in request.POST.getlist("ingredient[]"):
            ingredient =Ingredients.objects.get(id=id)
            cart.add(product=ingredient)
        return redirect("cart_detail")
    
@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Ingredients.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Ingredients.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Ingredients.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_detail(request):
    return render(request, 'cart.html')

@login_required(login_url="/login")
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url="/login")
def order_confirm_view(request):
    cart= Cart(request)
    cart.clear()
    return render(request,'order-confirm.html')
