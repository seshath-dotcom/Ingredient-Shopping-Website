from django.urls import path
from . import views
from .views import DishViewSet, IngredientsViewSet, home, recipe, recipeall
from django.urls import include, path
from rest_framework import routers
router =routers.SimpleRouter() 
router.register(r"dish",DishViewSet)
router.register(r"ingredient",IngredientsViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('',home,name="home"),
    path('recipe/<int:id>',recipe,name="recipe"),
    path('recipe-all',recipeall,name="recipe-all"),
    path('login',views.LoginInterfaceView.as_view()),
    path('signup',views.SignupView.as_view(),name='signup'),
    path('cart/multiadd/', views.cart_multiadd, name='cart_mulitadd'),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('logout',views.logout_view,name="logout"),
    path('order-confirm',views.order_confirm_view,name="order_confirm"),
    path('recipe/search',views.search,name="dish_search")
]

