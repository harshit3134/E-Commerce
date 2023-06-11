from django.urls import path, include
from vendor.views import form
urlpatterns=[
    path('forms/',form,name='form'),
]