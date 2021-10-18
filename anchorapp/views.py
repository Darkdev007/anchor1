import uuid
import json
import requests
from django.http.response import HttpResponse
from anchorapp.models import Category
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Category,Product,ShopCart
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView 

def index(request):
    Categories = Category.objects.all()[:3]
    bseller = Product.objects.filter(best_seller = True)
    dlatest = Product.objects.filter(latest = True)
    context = {
        'Categories' : Categories,
        'bseller' : bseller,
        'dlatest' : dlatest
    }
    return render(request, 'index.html',context)

def categories(request):
    Categories = Category.objects.all()
    context = {
        'Categories' : Categories
    }
    return render(request, "categories.html",context)

def products(request):
    Categories = Category.objects.all()
    Products = Product.objects.filter(available = True)
    context = {
        'Products' : Products,
        'Categories' : Categories
    }
    return render(request, 'products.html',context)

def product(request,id):
    Categories = Category.objects.all()
    product = Product.objects.get(pk=id)
    context = {
        'product' : product,
        'Categories' : Categories
    }
    return render(request,'product.html',context)

def category(request,id):
    Categories = Category.objects.all()
    category = Product.objects.filter(category_id = id)
    context = {
        'Categories': Categories,
        'category': category
    }
    return render(request, 'category.html',context)


def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            messages.success(request, 'You have successfully logged in')
            return redirect('index')
        else:
            messages.error(request, "Invalid Username/Password")
            return redirect('login')

    else:
        return render(request, 'login.html')

def logoutpage(request):
    logout(request)
    messages.success(request, 'You have logged out successfully')
    return redirect('login')


def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email is already in use')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=first_name, last_name=last_name,username=username,email=email,password=password)
                    user.save()
                    messages.success(request, 'You have successfully registered')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'register.html')

def passwordupdate(request):
    if request.method == 'POST':
        current = request.POST['password']
        new_password = request.POST['passwordnew']

        user = User.objects.get(id=request.user.id)
        check = user.check_password(current)
        if check == True:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password has successfully been changed')
            return redirect('login')
        else:
            messages.error(request, 'Incorrect Current password')
            return redirect('password')
    else:
        return render(request, 'password.html')

@login_required(login_url='loginpage')
def addtocart(request):
    if request.method == 'POST':
        basket_no = str(uuid.uuid4())
        vol = int(request.POST['itemquant'])
        pid = request.POST['itemid']
        itemid = Product.objects.get(pk=pid)
        cart = ShopCart.objects.filter(user__username= request.user.username, paid_item= False)
        if cart:
            basket = ShopCart.objects.filter(product_id = itemid.id ,user__username= request.user.username).first()
            if basket:
                basket.quantity += vol
                basket.save()
                messages.success(request, "You have added to your previous item")
                return redirect('products')
            else:
                newitem = ShopCart()
                newitem.user = request.user
                newitem.product = itemid
                newitem.quantity = vol
                newitem.paid_item = False
                newitem.cart_no = cart[0].cart_no
                newitem.save()
                messages.success(request, 'New item added to cart')
                return redirect('products')

        else:
            newbasket = ShopCart()
            newbasket.user = request.user
            newbasket.product = itemid
            newbasket.quantity = vol
            newbasket.paid_item = False
            newbasket.cart_no = basket_no
            newbasket.save()
            messages.success(request, 'A new item has been added to your cart')
            return redirect('products')

def cart(request):
    basket = ShopCart.objects.filter(user__username = request.user.username,paid_item = False)
    total = 0
    for item in basket:
        total += item.product.price * item.quantity
    context = {
        'basket': basket,
        'total': total
    }
    return render(request, 'cart.html',context)

def checkout(request):
    basket = ShopCart.objects.filter(user__username = request.user.username,paid_item = False)
    total = 0
    for item in basket:
        total += item.product.price * item.quantity
    context = {
        'basket': basket,
        'total': total,
        'order_code': basket[0].cart_no
    }
    return render(request, 'checkout.html', context)

def sendorder(request):
    if request.method == 'POST':
        api_key = 'sk_test_f0a5a8b92ea759bd42326fce0253c74bf3fc8ac9'
        curl = 'https://api.paystack.co/transaction/initialize'
        cburl = 'http://127.0.0.1:8000/completed'
        pay_num = str(uuid.uuid4())
        price = float(request.POST['price']) * 100
        user = User.objects.filter(username = request.user.username)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        phone = request.POST['phone']
        state = request.POST['state']
        bag_num = request.POST['bag']

        headers = {"Authorization" : f'Bearer{api_key}'}
        data = {
            'reference': pay_num,
            'email' : User.email,
            'amount' : int(price),
            'order_number' : bag_num,
            'callback_url' : cburl
        }

        try:
            r = requests.post(curl,headers=headers,json=data)
        except Exception:
            messages.error(request, 'unable to connect to paystack')
        else:
            transback = json.loads(r.text)
            rd_url = transback['data']['authorization_url']
            return redirect(rd_url)
    return redirect('checkout')

def completed(request):
    return render(request, 'completed.html')