from tkinter import E
from django.shortcuts import render, redirect
from products.models import Product, SizeVariant
from django.http import HttpResponse, HttpResponseRedirect


def get_product(request, slug):
    product = Product.objects.get(slug=slug)
    width = product.reviews*20 if  product.reviews != None else 0
    context = {'product': product, 'width': width}
    if request.GET.get('size'):
        size = request.GET.get('size')
        size_variant = product.size_variant.get(size_name=size)
        price = product.price + size_variant.price
        context['selected_size'] = size
        context['updated_price'] = price
        print(price)

    return render(request, 'product/product.html', context=context)

