from django.urls import path
from accounts.views import login_page, register_page, activate_email
from accounts.views import add_to_cart, cart_view, remove_cart,logout_page,payment_sucess

urlpatterns = [
    path('login/', login_page, name="login"),
    path('register/', register_page, name="register"),
    path('activate/<email_token>/', activate_email, name="activate_email"),
    path('cart/', cart_view, name="cart"),
    path('add-to-cart/<uid>/', add_to_cart, name="add_to_cart"),
    path('remove-cart/<cart_item_uid>/', remove_cart, name="remove_cart"),
    path('logout/',logout_page,name="logout"),
    path('success/',payment_sucess)
]
