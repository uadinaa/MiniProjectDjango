from django.urls import path

from . import views
from .views import (login_view, register_view,  admin_profile,
    seller_profile, trader_profile, customer_profile,
    purchase_history, customer_requests, customer_feed,
    add_product, seller_products, trader_products,
    add_trader_product, trader_all_products, customer_purchase_product,
    seller_requests, accept_request, deny_request,
    customer_receipts, print_receipt, trader_receipts, trader_requests, trader_purchase_product)

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import seller_products  # Import the view


urlpatterns = [
    path("login/", login_view, name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path("register/", register_view, name="register"),
    path("admin_page/", admin_profile, name="admin_page"),

    path("seller_profile/", seller_profile, name="seller_profile"),
    path("seller_profile/add_product/", add_product, name="add_product"),
    path("seller_profile/seller_products/", seller_products, name="seller_products"),
    path("seller_profile/seller_requests/", seller_requests, name="seller_requests"),
    path("accept_request/<int:request_id>/", accept_request, name="accept_request"),
    path("deny_request/<int:request_id>/", deny_request, name="deny_request"),

    path("trader_profile/", trader_profile, name="trader_profile"),
    path("trader_profile/add_trader_product/", add_trader_product, name="add_trader_product"),
    path('trader_profile/trader_products/', trader_products, name='trader_products'),
    path('trader_profile/trader_all_products/', trader_all_products, name='trader_all_products'),
    path('trader_profile/trader_receipts/', trader_receipts, name="trader_receipts"),
    path("trader_profile/trader_requests/", trader_requests, name="trader_requests"),
    path('trader_accept_request/<int:request_id>/', views.trader_accept_request, name='trader_accept_request'),
    path("trader_deny_request/<int:request_id>/", views.trader_deny_request, name="trader_deny_request"),
    path('trader_profile/trader_purchase_product/<int:product_id>/', trader_purchase_product,
         name='trader_purchase_product'),

    path("customer_profile/", customer_profile, name="customer_profile"),
    path('customer_profile/customer_feed/', customer_feed, name='customer_feed'),
    path('customer_profile/customer_requests/', customer_requests, name='customer_requests'),
    path('customer_profile/customer_purchase_product/<int:product_id>/', customer_purchase_product, name='customer_purchase_product'),
    path('customer_profile/customer_receipts/', customer_receipts, name="customer_receipts"),
    # path('customer_profile/purchase_history/', purchase_history, name='purchase_history'),

    path("print_receipt/<int:receipt_id>/", print_receipt, name="print_receipt"),
    path('pay/<int:request_id>/', views.pay_for_product, name='pay_for_product'),

]
