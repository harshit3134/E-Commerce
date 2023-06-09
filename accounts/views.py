from cmath import log
from tkinter import E
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from products.models import Product, SizeVariant
from .models import Cart, CartItems, Profile
from home.views import index
import razorpay
from django.conf import settings

def login_page(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)

        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username=email, password=password)
        if user_obj:
            login(request, user_obj)
            return redirect('/')

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/login.html')


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=email)
        if user_obj.exists():
            messages.warning(request, 'User Already Exist :) ')
            return HttpResponseRedirect(request.path_info)

        user_obj = User.objects.create(
            first_name=first_name, last_name=last_name, email=email, username=email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, 'A Verification has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/register.html')


def logout_page(request):
    logout(request)
    return redirect('index')

def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        return redirect('index')
    except Exception as e:
        return HttpResponse('Invalid Email token')


def add_to_cart(request, uid):
    variant = request.GET.get('variant')
    product = Product.objects.get(uid=uid)
    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

    cart_item = CartItems.objects.create(cart=cart, product=product)

    if variant:
        variant = request.GET.get('variant')
        size_variant = SizeVariant.objects.get(size_name=variant)
        cart_item.size_variant = size_variant
        cart_item.save()

    return redirect('index')

# def cart(request):
#     context={'cart':Cart.objects.filter(is_paid=False,user=request.user)}
#     return render(request,'accounts/cart.html',context)
def remove_cart(request,cart_item_uid):
    cart_item=CartItems.objects.get(uid=cart_item_uid)
    cart_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def cart_view(request):
    # Retrieve the user's cart
    cart = Cart.objects.get(user=request.user,is_paid = False)

    # Retrieve all cart items associated with the cart
    cart_items = CartItems.objects.filter(cart=cart)
    total = cart.get_cart_total()
    if int(total) > 0 :
        client = razorpay.Client(auth = (settings.KEY,settings.SECRET))
        payment = client.order.create({'amount' : cart.get_cart_total()*100,'currency': 'INR','payment_capture' : 1})
        cart.razorpay_order_id = payment['id']
        cart.save()
        context = {
            'cart': cart,
            'cart_items': cart_items,
            'payment' : payment
        }
    else:
        context = {
            'cart': cart,
            'cart_items': cart_items,
        }
    # print ("*******************")
    # print(payment)
    return render(request, 'accounts/cart.html', context)

def payment_sucess(request):
    order_id = request.GET.get('order_id')
    cart = Cart.objects.get(razorpay_order_id=order_id)
    cart.is_paid = True
    cart.save()
    return HttpResponse("Payment successful")
