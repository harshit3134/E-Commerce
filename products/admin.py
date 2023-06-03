from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price']
    inlines = [ProductImageAdmin]


@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size_name', 'price']
    model = SizeVariant


admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage)
