from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from requests import Response
from django.contrib import messages
from rest_framework import viewsets, generics, permissions

from .models import Seller, Trader, Purchase
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    SellerSerializer,
    TraderSerializer,
)
# way to import
from products.models import Product, Category, Store
from sales.models import PurchaseRequest, Receipt
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q



User = get_user_model()


def is_seller(user):
    return user.role == "seller"


def register_seller(user):
    seller = Seller(user=user, company_name="Your Company Name")
    seller.save()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


def register_view(request):
    if request.method == "POST":
        data = {
            "username": request.POST.get("username"),
            "email": request.POST.get("email"),
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "password": request.POST.get("password"),
            "role": request.POST.get("role"),
            "profile_picture": request.POST.get("profile_picture"),
        }

        serializer = UserRegistrationSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()

            login(request, user)  # Log the user in after successful registration
            messages.success(request, "Registration successful!")

            # Redirect based on role
            if user.role == "admin":
                return redirect("/api/users/admin_page/")
            elif user.role == "seller":
                return redirect("/api/users/seller_profile/")
            elif user.role == "trader":
                return redirect("/api/users/trader_profile/")
            else:
                return redirect("/api/users/customer_profile/")
        else:
            messages.error(request, "Error in registration. Please try again.")
            messages.error(request, f"Error: {serializer.errors}")
    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == "admin":
                return redirect("/api/users/admin_page/")
            elif user.role == "seller":
                return redirect("/api/users/seller_profile/")
            elif user.role == "trader":
                return redirect("/api/users/trader_profile/")
            else:
                return redirect("/api/users/customer_profile/")
    return render(request, "login.html")


def profile_view(request):
    purchases = Purchase.objects.filter(user=request.user)  # Покупки текущего пользователя
    return render(request, 'profile.html', {'purchases': purchases})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


@login_required
def seller_profile(request):
    user = request.user
    if request.method == "POST":
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.email = request.POST.get("email", user.email)

        if "profile_picture" in request.FILES:
            user.profile_picture = request.FILES["profile_picture"]

        user.save()

        # Update the seller's stores
        if request.user.role == 'seller':
            seller, created = Seller.objects.get_or_create(user=user)
            store_ids = request.POST.getlist("stores")
            stores = Store.objects.filter(id__in=store_ids)
            seller.stores.set(stores)
            seller.save()

        return redirect("seller_profile")

    stores = Store.objects.all()
    return render(request, "seller_profile.html", {"stores": stores})


@login_required
def add_product(request):
    if request.user.role != 'seller':
        return HttpResponse("You are not registered as a seller.", status=403)

    if request.method == "POST":
        name = request.POST["name"]
        price = request.POST["price"]
        description = request.POST["description"]
        image = request.FILES.get("image")
        stock = request.POST.get("stock", 0)
        category_id = request.POST.get("category")

        seller, created = Seller.objects.get_or_create(user=request.user)
        category = Category.objects.get(id=category_id)

        product = Product(
            seller=seller,
            name=name,
            price=price,
            description=description,
            image=image,
            stock=stock,
            category=category
        )
        product.save()

        return redirect("seller_products")

    categories = Category.objects.all()
    return render(request, "add_product.html", {"categories": categories})


@login_required
def seller_products(request):
    if request.user.role != 'seller':
        return HttpResponse("You are not registered as a seller.", status=403)

    seller, created = Seller.objects.get_or_create(user=request.user)
    products = Product.objects.filter(seller=seller)
    return render(request, "seller_feed.html", {"products": products})


@login_required
def seller_products(request):
    try:
        seller = Seller.objects.get(user=request.user)
        print(f"Seller found: {seller}")  # Debug print
    except Seller.DoesNotExist:
        print("Seller does not exist")  # Debug print
        return HttpResponse("Seller matching query does not exist.", status=403)

    products = Product.objects.filter(seller=seller)
    return render(request, "seller_feed.html", {"products": products})


@login_required
@user_passes_test(lambda user: user.role == "seller")
def seller_requests(request):
    seller = Seller.objects.get(user=request.user)
    requests = PurchaseRequest.objects.filter(product__seller=seller, status="pending")
    return render(request, "seller_requests.html", {"requests": requests})


@login_required
@user_passes_test(lambda user: user.role == "seller")
def accept_request(request, request_id):
    purchase_request = PurchaseRequest.objects.get(id=request_id)
    purchase_request.status = "accepted"
    purchase_request.save()
    messages.success(request, "Request accepted!")
    return redirect("seller_requests")


@login_required
@user_passes_test(lambda user: user.role == "seller")
def deny_request(request, request_id):
    purchase_request = PurchaseRequest.objects.get(id=request_id)
    purchase_request.status = "denied"
    purchase_request.save()
    messages.success(request, "Request denied!")
    return redirect("seller_requests")


class TraderViewSet(viewsets.ModelViewSet):
    queryset = Trader.objects.all()
    serializer_class = TraderSerializer


@login_required
@user_passes_test(lambda user: user.role == "trader")
def trader_profile(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.email = request.POST.get("email", user.email)
        user.role = request.POST.get("role", user.role)

        if "profile_picture" in request.FILES:
            user.profile_picture = request.FILES["profile_picture"]

        user.save()
        return redirect("trader_profile")  # Перенаправляет обратно после сохранения

    return render(request, "trader_profile.html")


@login_required
def add_trader_product(request):
    if request.user.role != 'trader':
        return HttpResponse("You are not registered as a trader.", status=403)

    if request.method == "POST":
        name = request.POST["name"]
        price = request.POST["price"]
        description = request.POST["description"]
        image = request.FILES.get("image")
        stock = request.POST.get("stock", 0)
        category_id = request.POST.get("category")

        trader, created = Trader.objects.get_or_create(user=request.user)
        category = Category.objects.get(id=category_id)

        product = Product(
            trader=trader,
            name=name,
            price=price,
            description=description,
            image=image,
            stock=stock,
            category=category
        )
        product.save()

        return redirect("trader_products")

    categories = Category.objects.all()
    return render(request, "add_trader_product.html", {"categories": categories})


# @login_required
# def trader_products(request):
#     if request.user.role != 'trader':
#         return HttpResponse("You are not registered as a trader.", status=403)
#
#     trader, _ = Trader.objects.get_or_create(user=request.user)  # Получаем или создаем Seller
#     products = Product.objects.filter(trader=trader)
#
#     return render(request, "trader_feed.html", {"products": products})
@login_required
def trader_products(request):
    if request.user.role != 'trader':
        return HttpResponse("You are not registered as a trader.", status=403)

    try:
        trader = Trader.objects.get(user=request.user)
        products = Product.objects.filter(trader=trader)
        return render(request, "trader_feed.html", {"products": products})
    except Trader.DoesNotExist:
        return HttpResponse("Trader does not exist.", status=403)


@login_required
def trader_all_products(request):
    if request.user.role != 'trader':
        return HttpResponse("You are not registered as a trader.", status=403)

    products = Product.objects.all()
    return render(request, 'trader_all_feed.html', {"products": products})


@login_required
@user_passes_test(lambda user: user.role == "trader")
def trader_pay_for_product(request, request_id):
    with transaction.atomic():
        purchase_request = PurchaseRequest.objects.select_for_update().get(id=request_id)
        trader = purchase_request.trader  # Трейдер и есть продавец
        product = purchase_request.product

        if trader.user.balance < product.price:
            messages.error(request, "Insufficient funds.")
            return redirect("trader_requests")

        trader.user.balance -= product.price
        trader.user.save()

        purchase_request.status = "paid"
        purchase_request.save()

    # Создаем чек
    receipt = Receipt.objects.create(
        trader=trader,
        product=product,
        price=product.price
    )

    # Добавляем покупку в таблицу Purchase
    purchase = Purchase.objects.create(
        trader=trader.user,
        product=product,
        price=product.price,
        purchase_date=timezone.now()
    )

    messages.success(request, "Payment successful! Receipt and purchase record created.")
    return redirect("trader_requests")


@login_required
def trader_purchase_product(request, product_id):
    try:
        trader = request.user.trader  # Ensure the user is a trader
    except ObjectDoesNotExist:
        return HttpResponse("Error: User is not associated with a trader.", status=400)

    # Assign the trader correctly instead of using the customer field
    request_obj = PurchaseRequest.objects.create(
        trader=trader,  # Use the 'trader' field instead of 'customer'
        product_id=product_id,
    )

    return redirect('trader_all_products')


# @login_required
# @user_passes_test(lambda user: user.role == "trader")
# def trader_requests(request):
#     try:
#         trader = Trader.objects.get(user=request.user)
#         requests = PurchaseRequest.objects.filter(product__trader=trader, status="pending")
#         return render(request, "trader_request.html", {"requests": requests})
#     except Trader.DoesNotExist:
#         return HttpResponse("Trader does not exist.", status=403)

# @login_required
# @user_passes_test(lambda user: user.role == "trader")
# def trader_requests(request):
#     try:
#         trader = Trader.objects.get(user=request.user)
#
#         # Requests where the trader is the buyer OR the trader is selling the product
#         requests = PurchaseRequest.objects.filter(
#             models.Q(product__trader=trader) | models.Q(trader=trader),
#             status="pending",
#         )
#
#         return render(request, "trader_request.html", {"requests": requests})
#     except Trader.DoesNotExist:
#         return HttpResponse("Trader does not exist.", status=403)

# @login_required
# @user_passes_test(lambda user: user.role == "trader")
# def trader_requests(request):
#     try:
#         trader = Trader.objects.get(user=request.user)
#
#         # Requests where the trader is the buyer OR the trader is selling the product
#         requests = PurchaseRequest.objects.filter(
#             Q(product__trader=trader) | Q(trader=trader),
#             status="pending",
#         )
#
#         return render(request, "trader_request.html", {"requests": requests})
#     except Trader.DoesNotExist:
#         return HttpResponse("Trader does not exist.", status=403)
#


@login_required
@user_passes_test(lambda user: user.role == "trader")
def trader_requests(request):
    try:
        trader = Trader.objects.get(user=request.user)

        # Requests where the trader wants to buy a product
        my_purchase_requests = PurchaseRequest.objects.filter(trader=trader, status="pending")

        # Requests from customers who want to buy trader's products
        incoming_requests = PurchaseRequest.objects.filter(product__trader=trader, status="pending")

        return render(
            request,
            "trader_request.html",
            {
                "my_purchase_requests": my_purchase_requests,
                "incoming_requests": incoming_requests,
            },
        )
    except Trader.DoesNotExist:
        return HttpResponse("Trader does not exist.", status=403)


@login_required
@user_passes_test(lambda user: user.role == "trader")
def trader_accept_request(request, request_id):
    purchase_request = PurchaseRequest.objects.get(id=request_id)
    purchase_request.status = "accepted"
    purchase_request.save()
    messages.success(request, "Request accepted!")
    return redirect("trader_requests")


@login_required
@user_passes_test(lambda user: user.role == "trader")
def trader_deny_request(request, request_id):
    purchase_request = PurchaseRequest.objects.get(id=request_id)
    purchase_request.status = "denied"
    purchase_request.save()
    messages.success(request, "Request denied!")
    return redirect("trader_requests")


# @login_required
# @user_passes_test(lambda user: user.role == "trader")
# def trader_receipts(request):
#     receipts = Receipt.objects.filter(trader=request.user.trader)
#     return render(request, "trader_receipts.html", {"receipts": receipts})

@login_required
@user_passes_test(lambda user: user.role == "trader")
def trader_receipts(request):
    try:
        trader = Trader.objects.get(user=request.user)  # Получаем трейдера

        receipts = Receipt.objects.filter(trader=trader)  # Используем seller, а не trader

        return render(request, "trader_receipts.html", {"receipts": receipts})
    except Trader.DoesNotExist:
        return HttpResponse("Trader does not exist.", status=403)


@login_required
@user_passes_test(lambda user: user.role == "trader")
def print_receipt(request, receipt_id):
    receipt = Receipt.objects.get(id=receipt_id)

    # Create the HTTP response with PDF content
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="receipt_{receipt.id}.pdf"'

    # Generate PDF using ReportLab
    p = canvas.Canvas(response)
    p.drawString(100, 800, f"Receipt ID: {receipt.id}")
    p.drawString(100, 780, f"Customer: {receipt.customer.user.username}")
    p.drawString(100, 760, f"Seller: {receipt.seller.user.username}")
    p.drawString(100, 740, f"Product: {receipt.product.name}")
    p.drawString(100, 720, f"Price: ${receipt.price}")

    p.showPage()
    p.save()

    return response


class TraderViewSet(viewsets.ModelViewSet):
    queryset = Trader.objects.all()
    serializer_class = TraderSerializer


@login_required
@user_passes_test(lambda user: user.role == "admin")
def admin_profile(request):
    users = User.objects.all().order_by("-role")
    return render(request, "admin_page.html", {"users": users})


@login_required
@user_passes_test(lambda user: user.role == "customer")
def customer_profile(request):
    user = request.user  # Получаем текущего пользователя

    if request.method == "POST":
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.email = request.POST.get("email", user.email)

        if "profile_picture" in request.FILES:
            user.profile_picture = request.FILES["profile_picture"]  # Загружаем файл

        user.save()
        return redirect("customer_profile")  # Обновление страницы

    return render(request, "customer_profile.html")


def customer_feed(request):
    products = Product.objects.all()
    return render(request, "customer_feed.html", {"products": products})


@login_required
@user_passes_test(lambda user: user.role == "customer")
def customer_purchase_product(request, product_id):
    try:
        customer = request.user.customer  # Try to access the related Customer
    except ObjectDoesNotExist:
        return HttpResponse("Error: User is not associated with a customer.", status=400)

    product = Product.objects.get(id=product_id)

    # Создаем заявку на покупку
    request_obj = PurchaseRequest.objects.create(
        customer=request.user.customer,
        product=product,
        status="pending"
    )

    messages.success(request, "Request to buy was sent.")
    return redirect("customer_feed")


@login_required
@user_passes_test(lambda user: user.role == "customer")
def customer_requests(request):
    requests = PurchaseRequest.objects.filter(customer=request.user.customer).order_by("-id")
    return render(request, "customer_requests.html", {"requests": requests})


@login_required
@user_passes_test(lambda user: user.role == "customer")
def purchase_history(request):
    # purchases = Purchase.objects.filter(customer=request.user.customer).order_by("-purchase_date")
    purchases = Purchase.objects.filter(user=request.user).order_by("-purchased_at")
    return render(request, "purchase_history.html", {"purchases": purchases})



@login_required
@user_passes_test(lambda user: user.role == "customer")
def pay_for_product(request, request_id):
    with transaction.atomic():
        purchase_request = PurchaseRequest.objects.select_for_update().get(id=request_id)
        customer = purchase_request.customer
        product = purchase_request.product
        seller = product.seller.user

        if customer.user.balance < product.price:
            messages.error(request, "Insufficient funds.")
            return redirect("customer_requests")

        customer.user.balance -= product.price
        seller.balance += product.price
        customer.user.save()
        seller.save()

        purchase_request.status = "paid"
        purchase_request.save()

    # Создаем чек
    receipt = Receipt.objects.create(
        customer=customer,
        seller=product.seller,
        product=product,
        price=product.price
    )

    # Добавляем покупку в таблицу Purchase
    purchase = Purchase.objects.create(
        customer=customer.user,
        product=product,
        price=product.price,
        purchase_date=timezone.now()
    )

    # messages.success(request, "Payment successful! Receipt and purchase record created.")
    return redirect("customer_requests")


@login_required
@user_passes_test(lambda user: user.role == "customer")
def customer_receipts(request):
    receipts = Receipt.objects.filter(customer=request.user.customer)
    return render(request, "customer_receipts.html", {"receipts": receipts})


def generate_pdf():
    pdf_file = "output.pdf"
    c = canvas.Canvas(pdf_file)

    # Add some text
    c.drawString(100, 750, "Hello, PDF!")

    # Save the PDF
    c.save()
    print(f"PDF saved as {pdf_file}")

generate_pdf()


@login_required
@user_passes_test(lambda user: user.role == "customer")
def print_receipt(request, receipt_id):
    receipt = Receipt.objects.get(id=receipt_id)

    # Create the HTTP response with PDF content
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="receipt_{receipt.id}.pdf"'

    # Generate PDF using ReportLab
    p = canvas.Canvas(response)
    p.drawString(100, 800, f"Receipt ID: {receipt.id}")
    p.drawString(100, 780, f"Customer: {receipt.customer.user.username}")
    p.drawString(100, 760, f"Seller: {receipt.seller.user.username}")
    p.drawString(100, 740, f"Product: {receipt.product.name}")
    p.drawString(100, 720, f"Price: ${receipt.price}")

    p.showPage()
    p.save()

    return response
