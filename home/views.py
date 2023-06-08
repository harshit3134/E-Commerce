from django.shortcuts import render
from products.models import Product
from django.db.models import Q

def index(request):

    context = {'products': Product.objects.all()}
    return render(request, 'home/index.html', context)

def search(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    products = Product.objects.filter(
        Q(category__category_name__icontains = q)|
        Q(product_name__icontains = q)|
        Q(author__icontains = q)
        )
    context = {'products' : products}

    return render(request, 'home/index.html',context)