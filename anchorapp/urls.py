from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = "index"),
    path('categories',views.categories, name = "categories"),
    path('products',views.products, name = "products"),
    path('product/<str:id>',views.product, name = "product"),
    path('category/<str:id>',views.product, name = "category"),
    path('login',views.loginpage, name = "login"),
    path('logout',views.logoutpage, name = "logout"),
    path('register',views.register, name = "register"),
    path('password',views.passwordupdate, name = "password"),
    path('addtocart',views.addtocart, name = "addtocart"),
    path('cart',views.cart, name = "cart"),
    path('checkout',views.checkout, name = "checkout"),
    path('sendorder',views.sendorder, name = "sendorder"),
    path('completed',views.completed, name = "completed"),
    
]