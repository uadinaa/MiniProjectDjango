# from django.test import TestCase
#
# # Create your tests here.
# # keke love trader
# # kiki love seller
# # lele love customer
#
#
#
#
# def product_creation(request, role, model, redirect_url):
#     if request.user.role != role:
#         return HttpResponse(f"You are not registered as a {role}.", status=403)
#
#     if request.method == "POST":
#         name = request.POST["name"]
#         price = request.POST["price"]
#         description = request.POST["description"]
#         image = request.FILES.get("image")
#         stock = request.POST.get("stock", 0)
#         category_id = request.POST.get("category")
#
#         seller_or_trader, _ = model.objects.get_or_create(user=request.user)
#         category = Category.objects.get(id=category_id)
#
#         product = Product(
#             seller=seller_or_trader,
#             name=name,
#             price=price,
#             description=description,
#             image=image,
#             stock=stock,
#             category=category
#         )
#         product.save()
#
#         return redirect(redirect_url)
#
#     categories = Category.objects.all()
#     # return render(request, "add_product.html", {"categories": categories}
#     return render(request, "add_product.html", {
#         "categories": categories,
#         "role": role,
#         "action_url": redirect_url,
#         "profile_url": f"{role}_profile",
#     })
#
# and I am using
# def seller_add_product(request):
#     product_creation(request, 'seller', Seller, 'seller_products')
# this and
# this
# def trader_add_product(request):
#     product_creation(request, 'trader', Trader, 'trader_products')
#
#
#
# <h2>Add {{ role|title }} Product</h2>
#
# <form action="{% url action_url %}" method="post" enctype="multipart/form-data">
#     {% csrf_token %}
#     <input type="text" name="name" placeholder="Product Name" required>
#     <input type="number" name="price" placeholder="Price" step="0.01" required>
#     <textarea name="description" placeholder="Description" required></textarea>
#     <label>Upload Image:</label>
#     <input type="file" name="image">
#     <input type="number" name="stock" placeholder="Stock" value="0" required>
#     <label>Select Category:</label>
#     <select name="category" required>
#         {% for category in categories %}
#             <option value="{{ category.id }}">{{ category.name }}</option>
#         {% endfor %}
#     </select>
#     <button type="submit">Add Product</button>
# </form>
#
# <a href="{% url profile_url %}">Back to Profile</a>
#
#
#
#
#
#
# @login_required
# def add_product(request):
#     if request.user.role != 'seller':
#         return HttpResponse("You are not registered as a seller.", status=403)
#
#     if request.method == "POST":
#         name = request.POST["name"]
#         price = request.POST["price"]
#         description = request.POST["description"]
#         image = request.FILES.get("image")
#         stock = request.POST.get("stock", 0)
#         category_id = request.POST.get("category")
#
#         seller, created = Seller.objects.get_or_create(user=request.user)
#         category = Category.objects.get(id=category_id)
#
#         product = Product(
#             seller=seller,
#             name=name,
#             price=price,
#             description=description,
#             image=image,
#             stock=stock,
#             category=category
#         )
#         product.save()
#
#         return redirect("seller_products")
#
#     categories = Category.objects.all()
#     return render(request, "add_product.html", {"categories": categories})














#
# это мои селлерс профиль
# <h1>Welcome, {{ user.username }}</h1>
#
# <!-- Profile Viewing Section -->
# <div id="profile-section">
#     <h2>Profile</h2>
#     <p><strong>Name:</strong> {{ user.first_name }}</p>
#     <p><strong>Last name:</strong> {{ user.last_name }}</p>
#     <p><strong>Email:</strong> {{ user.email }}</p>
#     <p><strong>Role:</strong>{{ user.role }}</p>
#
#     {% if user.profile_picture %}
#         <img src="{{ user.profile_picture.url }}" alt="Profile Picture" width="150">
#     {% else %}
#         <p>No profile picture uploaded.</p>
#     {% endif %}
#     <button onclick="showSection('edit-profile-section')">Edit</button>
# </div>
#
# <!-- Profile Editing Section -->
# <div id="edit-profile-section" style="display: none;">
#     <h2>Edit Profile</h2>
#     <form method="POST" enctype="multipart/form-data" action="{% url 'seller_profile' %}">
#         {% csrf_token %}
#         <input type="text" name="first_name" value="{{ user.first_name }}" placeholder="Name">
#         <input type="text" name="last_name" value="{{ user.last_name }}" placeholder="Last name">
#         <input type="email" name="email" value="{{ user.email }}" placeholder="Email">
#
#         <label>Upload Profile Picture:</label>
#         <input type="file" name="profile_picture">
#
#         <button type="submit">Save</button>
#     </form>
#     <button onclick="showSection('profile-section')">Cancel</button>
# </div>
#
# <!--&lt;!&ndash; Store Selection Section &ndash;&gt;-->
# <!--<form method="POST" enctype="multipart/form-data" action="{% url 'seller_profile' %}">-->
# <!--    {% csrf_token %}-->
# <!--    <h2>Select Stores</h2>-->
# <!--    <label>Select Stores:</label>-->
# <!--    <select name="stores" multiple>-->
# <!--        {% for store in stores %}-->
# <!--            <option value="{{ store.id }}">{{ store.name }}</option>-->
# <!--        {% endfor %}-->
# <!--    </select>-->
# <!--    <button type="submit">Update</button>-->
# <!--</form>-->
#
# <!-- Navigation Buttons -->
# <button onclick="window.location.href='/seller_profile/add_product/'">Add Product</button>
# <button onclick="window.location.href='/seller_profile/seller_products/'">View your products</button>
# <button onclick="window.location.href='/seller_profile/requests/'">Requests</button>
# <button onclick="window.location.href='/logout/'">Log out</button>
#
# <!-- JavaScript to Toggle Sections -->
# <script>
#     function showSection(section) {
#         document.getElementById('profile-section').style.display = 'none';
#         document.getElementById('edit-profile-section').style.display = 'none';
#         document.getElementById(section).style.display = 'block';
#     }
# </script>




# и селлерс посты:
# <h2>Your Products</h2>
#
# {% if products %}
#     <ul>
#         {% for product in products %}
#             <li>
#                 <strong>{{ product.name }}</strong> - ${{ product.price }}
#                 <p>{{ product.description }}</p>
#                 {% if product.image %}
#                     <img src="{{ product.image.url }}" alt="{{ product.name }}" width="150">
#                 {% endif %}
#             </li>
#         {% endfor %}
#     </ul>
# {% else %}
#     <p>No products added yet.</p>
# {% endif %}
#
# <a href="{% url 'seller_profile' %}">Back to Profile</a>
#



# и вот теперь мне по сути нужно тоже самое что в селлере, в трейдер. это мои трейдер профиль фа
#
# <h1>Welcome, {{ user.username }}</h1>
#
# <!-- Кнопки навигации -->
# <!--<button onclick="showSection('profile')">Profile</button>-->
#
#
# <!-- Раздел просмотра профиля -->
# <div id="profile-section">
#     <h2>Profile</h2>
#     <p><strong>Name:</strong> {{ user.first_name }}</p>
#     <p><strong>Last name:</strong> {{ user.last_name }}</p>
#     <p><strong>Email:</strong> {{ user.email }}</p>
#
#     {% if user.profile_picture %}
#         <img src="{{ user.profile_picture.url }}" alt="Profile Picture" width="150">
#     {% else %}
#         <p>No profile picture uploaded.</p>
#     {% endif %}
#
#     <button onclick="showSection('edit-profile')">Edit</button>
# </div>
#
# <!-- Раздел редактирования профиля -->
# <div id="edit-profile-section" style="display: none;">
#     <h2>Edit Profile</h2>
#     <form method="POST" enctype="multipart/form-data">
#         {% csrf_token %}
#         <input type="text" name="first_name" value="{{ user.first_name }}" placeholder="Name">
#         <input type="text" name="last_name" value="{{ user.last_name }}" placeholder="Last name">
#         <input type="email" name="email" value="{{ user.email }}" placeholder="Email">
#
#         <label>Upload Profile Picture:</label>
#         <input type="file" name="profile_picture">
#
#         <button type="submit">Save</button>
#     </form>
#     <button onclick="showSection('profile')">Cancel</button>
# </div>
#
# <button onclick="window.location.href='/seller/products/'">View Products</button>
# <button onclick="window.location.href='/seller/requests/'">Requests</button>
# <button onclick="window.location.href='/logout/'">Log out</button>
#
# <!-- JavaScript для переключения разделов -->
# <script>
#     function showSection(section) {
#         document.getElementById('profile-section').style.display = 'none';
#         document.getElementById('edit-profile-section').style.display = 'none';
#
#         if (section === 'profile') {
#             document.getElementById('profile-section').style.display = 'block';
#         } else if (section === 'edit-profile') {
#             document.getElementById('edit-profile-section').style.display = 'block';
#         }
#     }
# </script>
#



#
# это вьюшки
# # from django.shortcuts import render, redirect
# # from rest_framework import viewsets
# # from rest_framework import generics, permissions
# # from rest_framework_simplejwt.views import TokenObtainPairView
# # from django.contrib.auth import login, authenticate
# # from django.contrib.auth.decorators import login_required
# # from .models import Seller, Trader
# # from .serializers import UserRegistrationSerializer
# # from django.contrib.auth import get_user_model
# # from .serializers import UserSerializer, SellerSerializer, TraderSerializer
# #
# # User = get_user_model()
# #
# #
# # class RegisterView(generics.CreateAPIView):
# #     queryset = User.objects.all()
# #     serializer_class = UserRegistrationSerializer
# #     permission_classes = [permissions.AllowAny]
# #
# # def login_view(request):
# #     if request.method == "POST":
# #         username = request.POST.get("username")
# #         password = request.POST.get("password")
# #         user = authenticate(request, username=username, password=password)
# #         if user is not None:
# #             login(request, user)
# #             if user.role == "admin":
# #                 return redirect("/admin_dashboard/")
# #             elif user.role == "seller":
# #                 return redirect("/seller_dashboard/")
# #             elif user.role == "trader":
# #                 return redirect("/trader_dashboard/")
# #             else:
# #                 return redirect("/customer_dashboard/")
# #     return render(request, "login.html")
# #
# #
# # class LoginView(generics.GenericAPIView):
# #     permission_classes = [permissions.AllowAny]
# #
# #
# # class UserViewSet(viewsets.ModelViewSet):
# #     queryset = User.objects.all()
# #     serializer_class = UserSerializer
# #
# #     def get_queryset(self):
# #         return User.objects.all() or User.objects.none()
# #
# #
# # class SellerViewSet(viewsets.ModelViewSet):
# #     queryset = Seller.objects.all()
# #     serializer_class = SellerSerializer
# #
# #
# # class TraderViewSet(viewsets.ModelViewSet):
# #     queryset = Trader.objects.all()
# #     serializer_class = TraderSerializer
# from django.http import HttpResponse
# from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.decorators import login_required, user_passes_test
# from django.contrib.auth import get_user_model
# from requests import Response
# from django.contrib import messages
# from rest_framework import viewsets, generics, permissions
# from .models import Seller, Trader
# from .serializers import (
#     UserRegistrationSerializer,
#     UserSerializer,
#     SellerSerializer,
#     TraderSerializer,
# )
# # way to import
# from products.models import Product, Category, Store
#
#
# User = get_user_model()
#
#
# def is_seller(user):
#     return user.role == "seller"
#
#
# def register_seller(user):
#     seller = Seller(user=user, company_name="Your Company Name")
#     seller.save()
#
#
# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserRegistrationSerializer
#     permission_classes = [permissions.AllowAny]
#
#
# def register_view(request):
#     if request.method == "POST":
#         data = {
#             "username": request.POST.get("username"),
#             "email": request.POST.get("email"),
#             "first_name": request.POST.get("first_name"),
#             "last_name": request.POST.get("last_name"),
#             "password": request.POST.get("password"),
#             "role": request.POST.get("role"),
#             "profile_picture": request.POST.get("profile_picture"),
#         }
#
#         serializer = UserRegistrationSerializer(data=data)
#
#         if serializer.is_valid():
#             user = serializer.save()
#
#             login(request, user)  # Log the user in after successful registration
#             messages.success(request, "Registration successful!")
#
#             # Redirect based on role
#             if user.role == "admin":
#                 return redirect("/api/users/admin_page/")
#             elif user.role == "seller":
#                 return redirect("/api/users/seller_profile/")
#             elif user.role == "trader":
#                 return redirect("/api/users/trader_profile/")
#             else:
#                 return redirect("/api/users/customer_profile/")
#         else:
#             messages.error(request, "Error in registration. Please try again.")
#             messages.error(request, f"Error: {serializer.errors}")
#     return render(request, "register.html")
#
#
# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             if user.role == "admin":
#                 return redirect("/api/users/admin_page/")
#             elif user.role == "seller":
#                 return redirect("/api/users/seller_profile/")
#             elif user.role == "trader":
#                 return redirect("/api/users/trader_profile/")
#             else:
#                 return redirect("/api/users/customer_profile/")
#     return render(request, "login.html")
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class SellerViewSet(viewsets.ModelViewSet):
#     queryset = Seller.objects.all()
#     serializer_class = SellerSerializer
#
#
# @login_required
# def seller_profile(request):
#     user = request.user
#     if request.method == "POST":
#         user.first_name = request.POST.get("first_name", user.first_name)
#         user.last_name = request.POST.get("last_name", user.last_name)
#         user.email = request.POST.get("email", user.email)
#
#         if "profile_picture" in request.FILES:
#             user.profile_picture = request.FILES["profile_picture"]
#
#         user.save()
#
#         # Update the seller's stores
#         if request.user.role == 'seller':
#             seller, created = Seller.objects.get_or_create(user=user)
#             store_ids = request.POST.getlist("stores")
#             stores = Store.objects.filter(id__in=store_ids)
#             seller.stores.set(stores)
#             seller.save()
#
#         return redirect("seller_profile")
#
#     stores = Store.objects.all()
#     return render(request, "seller_profile.html", {"stores": stores})
#
# # @login_required
# # def add_product(request):
# #     try:
# #         seller = Seller.objects.get(user=request.user)
# #         print(f"Seller found: {seller}")  # Debug print
# #     except Seller.DoesNotExist:
# #         print("Seller does not exist")  # Debug print
# #         return HttpResponse("You are not registered as a seller.", status=403)
# #
# #     if request.method == "POST":
# #         name = request.POST["name"]
# #         price = request.POST["price"]
# #         description = request.POST["description"]
# #         image = request.FILES.get("image")
# #
# #         product = Product(seller=seller, name=name, price=price, description=description, image=image)
# #         product.save()
# #
# #         return redirect("seller_products")
# #
# #     return render(request, "add_product.html")
#
#
# @login_required
# def add_product(request):
#     if request.user.role != 'seller':
#         return HttpResponse("You are not registered as a seller.", status=403)
#
#     if request.method == "POST":
#         name = request.POST["name"]
#         price = request.POST["price"]
#         description = request.POST["description"]
#         image = request.FILES.get("image")
#         stock = request.POST.get("stock", 0)
#         category_id = request.POST.get("category")
#
#         seller, created = Seller.objects.get_or_create(user=request.user)
#         category = Category.objects.get(id=category_id)
#
#         product = Product(
#             seller=seller,
#             name=name,
#             price=price,
#             description=description,
#             image=image,
#             stock=stock,
#             category=category
#         )
#         product.save()
#
#         return redirect("seller_products")
#
#     categories = Category.objects.all()
#     return render(request, "add_product.html", {"categories": categories})
#
#
# # @login_required
# # def seller_products(request):
# #     seller = Seller.objects.get(user=request.user)
# #     products = Product.objects.filter(seller=seller)
# #     return render(request, "seller_feed.html", {"products": products})
#
# @login_required
# def seller_products(request):
#     if request.user.role != 'seller':
#         return HttpResponse("You are not registered as a seller.", status=403)
#
#     seller, created = Seller.objects.get_or_create(user=request.user)
#     products = Product.objects.filter(seller=seller)
#     return render(request, "seller_feed.html", {"products": products})
#
# @login_required
# def seller_products(request):
#     try:
#         seller = Seller.objects.get(user=request.user)
#         print(f"Seller found: {seller}")  # Debug print
#     except Seller.DoesNotExist:
#         print("Seller does not exist")  # Debug print
#         return HttpResponse("Seller matching query does not exist.", status=403)
#
#     products = Product.objects.filter(seller=seller)
#     return render(request, "seller_feed.html", {"products": products})
#
#
# class TraderViewSet(viewsets.ModelViewSet):
#     queryset = Trader.objects.all()
#     serializer_class = TraderSerializer
#
#
# @login_required
# @user_passes_test(lambda user: user.role == "trader")
# def trader_profile(request):
#     if request.method == "POST":
#         user = request.user
#         user.first_name = request.POST.get("first_name", user.first_name)
#         user.last_name = request.POST.get("last_name", user.last_name)
#         user.email = request.POST.get("email", user.email)
#         user.role = request.POST.get("role", user.role)
#
#         if "profile_picture" in request.FILES:
#             user.profile_picture = request.FILES["profile_picture"]
#
#         user.save()
#         return redirect("trader_profile")  # Перенаправляет обратно после сохранения
#
#     return render(request, "trader_profile.html")
#
# # Dashboard Views
#
#
# @login_required
# @user_passes_test(lambda user: user.role == "admin")
# def admin_profile(request):
#     users = User.objects.all().order_by("-role")
#     return render(request, "admin_page.html", {"users": users})
#
#
# @login_required
# @user_passes_test(lambda user: user.role == "customer")
# def customer_profile(request):
#     user = request.user  # Получаем текущего пользователя
#
#     if request.method == "POST":
#         user.first_name = request.POST.get("first_name", user.first_name)
#         user.last_name = request.POST.get("last_name", user.last_name)
#         user.email = request.POST.get("email", user.email)
#
#         if "profile_picture" in request.FILES:
#             user.profile_picture = request.FILES["profile_picture"]  # Загружаем файл
#
#         user.save()
#         return redirect("customer_profile")  # Обновление страницы
#
#     return render(request, "customer_profile.html")
#
#
# def customer_feed(request):
#     return render(request, 'customer_feed.html')
#
#
# def customer_requests(request):
#     return render(request, 'customer_request.html')
#
#
# def purchase_history(request):
#     return render(request, 'purchase_history.html')
#



# <!--<h2>Add {{ role|title }} Product</h2>-->
#
# <!--<form action="{% url action_url %}" method="post" enctype="multipart/form-data">-->
# <!--    {% csrf_token %}-->
# <!--    <input type="text" name="name" placeholder="Product Name" required>-->
# <!--    <input type="number" name="price" placeholder="Price" step="0.01" required>-->
# <!--    <textarea name="description" placeholder="Description" required></textarea>-->
# <!--    <label>Upload Image:</label>-->
# <!--    <input type="file" name="image">-->
# <!--    <input type="number" name="stock" placeholder="Stock" value="0" required>-->
# <!--    <label>Select Category:</label>-->
# <!--    <select name="category" required>-->
# <!--        {% for category in categories %}-->
# <!--            <option value="{{ category.id }}">{{ category.name }}</option>-->
# <!--        {% endfor %}-->
# <!--    </select>-->
# <!--    <button type="submit">Add Product</button>-->
# <!--</form>-->
#
# <!--<a href="{% url profile_url %}">Back to Profile</a>-->
#
#
# <!--<h2>All Products</h2>-->
#
# <!--{% if products %}-->
# <!--    <ul>-->
# <!--        {% for product in products %}-->
# <!--            <li>-->
# <!--                <strong>{{ product.name }}</strong> - ${{ product.price }}-->
# <!--                <p>{{ product.description }}</p>-->
# <!--                {% if product.image %}-->
# <!--                    <img src="{{ product.image.url }}" alt="{{ product.name }}" width="150">-->
# <!--                {% endif %}-->
# <!--            </li>-->
# <!--        {% endfor %}-->
# <!--    </ul>-->
# <!--{% else %}-->
# <!--    <p>No products added yet.</p>-->
# <!--{% endif %}-->
#
# <!--<a href="{% url 'customer_profile' %}">Back to Profile</a>-->

# @login_required
# def add_product(request):
#     try:
#         seller = Seller.objects.get(user=request.user)
#         print(f"Seller found: {seller}")  # Debug print
#     except Seller.DoesNotExist:
#         print("Seller does not exist")  # Debug print
#         return HttpResponse("You are not registered as a seller.", status=403)
#
#     if request.method == "POST":
#         name = request.POST["name"]
#         price = request.POST["price"]
#         description = request.POST["description"]
#         image = request.FILES.get("image")
#
#         product = Product(seller=seller, name=name, price=price, description=description, image=image)
#         product.save()
#
#         return redirect("seller_products")
#
#     return render(request, "add_product.html")

# @login_required
# @user_passes_test(lambda user: user.role == "customer")
# def print_receipt(request, receipt_id):
#     receipt = get_object_or_404(Receipt, id=receipt_id)
#
#     # Create the HTTP response with PDF headers
#     response = HttpResponse(content_type="application/pdf")
#     response["Content-Disposition"] = f'attachment; filename="receipt_{receipt.id}.pdf"'
#
#     # Create PDF document
#     doc = SimpleDocTemplate(response, pagesize=letter)
#     styles = getSampleStyleSheet()
#     content = []
#
#     # Add content to the PDF
#     content.append(Paragraph(f"<b>Receipt ID:</b> {receipt.id}", styles["Normal"]))
#     content.append(Spacer(1, 0.2 * inch))
#
#     content.append(Paragraph(f"<b>Customer:</b> {receipt.customer.user.username}", styles["Normal"]))
#     content.append(Paragraph(f"<b>Seller:</b> {receipt.seller.user.username}", styles["Normal"]))
#     content.append(Paragraph(f"<b>Product:</b> {receipt.product.name}", styles["Normal"]))
#     content.append(Paragraph(f"<b>Price:</b> ${receipt.price:.2f}", styles["Normal"]))
#     content.append(Spacer(1, 0.5 * inch))
#
#     content.append(Paragraph("Thank you for your purchase!", styles["Normal"]))
#
#     # Build the PDF
#     doc.build(content)
#     return response


# def purchase_history(request):
#     return render(request, 'purchase_history.html')

#
# @login_required
# @user_passes_test(lambda user: user.role == "customer")
# def pay_for_product(request, request_id):
#     purchase_request = PurchaseRequest.objects.get(id=request_id)
#
#     if purchase_request.status != "accepted":
#         return HttpResponse("Error: Request is not accepted.", status=400)
#
#     customer = purchase_request.customer
#     product = purchase_request.product
#     seller = product.seller.user
#
#     if customer.user.balance < product.price:
#         messages.error(request, "Insufficient funds.")
#         return redirect("customer_requests")
#
#     # Списание денег у покупателя
#     customer.user.balance -= product.price
#     customer.user.save()
#
#     # Пополнение баланса продавца
#     seller.balance += product.price
#     seller.save()
#
#     # Обновляем статус заявки
#     purchase_request.status = "paid"
#     purchase_request.save()
#
#     # Создаем чек
#     receipt = Receipt.objects.create(
#         customer=customer,
#         seller=product.seller,
#         product=product,
#         price=product.price
#     )
#
#     messages.success(request, "Payment successful! Receipt generated.")
#     return redirect("customer_requests")



# from django.shortcuts import render, redirect
# from rest_framework import viewsets
# from rest_framework import generics, permissions
# from rest_framework_simplejwt.views import TokenObtainPairView
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.decorators import login_required
# from .models import Seller, Trader
# from .serializers import UserRegistrationSerializer
# from django.contrib.auth import get_user_model
# from .serializers import UserSerializer, SellerSerializer, TraderSerializer
#
# User = get_user_model()
#
#
# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserRegistrationSerializer
#     permission_classes = [permissions.AllowAny]
#
# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             if user.role == "admin":
#                 return redirect("/admin_dashboard/")
#             elif user.role == "seller":
#                 return redirect("/seller_dashboard/")
#             elif user.role == "trader":
#                 return redirect("/trader_dashboard/")
#             else:
#                 return redirect("/customer_dashboard/")
#     return render(request, "login.html")
#
#
# class LoginView(generics.GenericAPIView):
#     permission_classes = [permissions.AllowAny]
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     def get_queryset(self):
#         return User.objects.all() or User.objects.none()
#
#
# class SellerViewSet(viewsets.ModelViewSet):
#     queryset = Seller.objects.all()
#     serializer_class = SellerSerializer
#
#
# class TraderViewSet(viewsets.ModelViewSet):
#     queryset = Trader.objects.all()
#     serializer_class = TraderSerializer
from time import timezone

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse










#
# from django.shortcuts import render, redirect
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.decorators import login_required, user_passes_test
# from django.contrib.auth import get_user_model
# from requests import Response
# from django.contrib import messages
# from rest_framework import viewsets, generics, permissions
# from .models import Seller, Trader
# from .serializers import (
#     UserRegistrationSerializer,
#     UserSerializer,
#     SellerSerializer,
#     TraderSerializer,
# )
# # way to import
# from products.models import Product, Category, Store
# import logging
# from django.http import HttpResponse
#
# def debug_view(request):
#     return HttpResponse(f"Resolver Match: {request.resolver_match}")
#
#
# logger = logging.getLogger(__name__)
#
#
# User = get_user_model()
#
#
# def is_seller(user):
#     return user.role == "seller"
#
#
# def register_seller(user):
#     seller = Seller(user=user, company_name="Your Company Name")
#     seller.save()
#
#
# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserRegistrationSerializer
#     permission_classes = [permissions.AllowAny]
#
#
# def register_view(request):
#     if request.method == "POST":
#         data = {
#             "username": request.POST.get("username"),
#             "email": request.POST.get("email"),
#             "first_name": request.POST.get("first_name"),
#             "last_name": request.POST.get("last_name"),
#             "password": request.POST.get("password"),
#             "role": request.POST.get("role"),
#             "profile_picture": request.POST.get("profile_picture"),
#         }
#
#         serializer = UserRegistrationSerializer(data=data)
#
#         if serializer.is_valid():
#             user = serializer.save()
#
#             login(request, user)  # Log the user in after successful registration
#             messages.success(request, "Registration successful!")
#
#             # Redirect based on role
#             if user.role == "admin":
#                 return redirect("/api/users/admin_page/")
#             elif user.role == "seller":
#                 return redirect("/api/users/seller_profile/")
#             elif user.role == "trader":
#                 return redirect("/api/users/trader_profile/")
#             else:
#                 return redirect("/api/users/customer_profile/")
#         else:
#             messages.error(request, "Error in registration. Please try again.")
#             messages.error(request, f"Error: {serializer.errors}")
#     return render(request, "register.html")
#
#
# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             if user.role == "admin":
#                 return redirect("/api/users/admin_page/")
#             elif user.role == "seller":
#                 return redirect("/api/users/seller_profile/")
#             elif user.role == "trader":
#                 return redirect("/api/users/trader_profile/")
#             else:
#                 return redirect("/api/users/customer_profile/")
#     return render(request, "login.html")
#
#
# # @login_required
# # def add_product(request):
# #     if request.user.role != 'seller':
# #         return HttpResponse("You are not registered as a seller.", status=403)
# #
# #     if request.method == "POST":
# #         name = request.POST["name"]
# #         price = request.POST["price"]
# #         description = request.POST["description"]
# #         image = request.FILES.get("image")
# #         stock = request.POST.get("stock", 0)
# #         category_id = request.POST.get("category")
# #
# #         seller, created = Seller.objects.get_or_create(user=request.user)
# #         category = Category.objects.get(id=category_id)
# #
# #         product = Product(
# #             seller=seller,
# #             name=name,
# #             price=price,
# #             description=description,
# #             image=image,
# #             stock=stock,
# #             category=category
# #         )
# #         product.save()
# #
# #         return redirect("seller_products")
# #
# #     categories = Category.objects.all()
# #     return render(request, "add_product.html", {"categories": categories})
#
# def product_creation(request, role, model, redirect_url):
#     if request.user.role != role:
#         logger.error(f"User {request.user.username} is not a {role}.")
#         return HttpResponse(f"You are not registered as a {role}.", status=403)
#
#     if request.method == "POST":
#         logger.info("Received POST request.")
#         name = request.POST["name"]
#         price = request.POST["price"]
#         description = request.POST["description"]
#         image = request.FILES.get("image")
#         stock = request.POST.get("stock", 0)
#         category_id = request.POST.get("category")
#
#         logger.info(f"Form data received: name={name}, price={price}, description={description}, stock={stock}, category_id={category_id}")
#
#         seller_or_trader, created = model.objects.get_or_create(user=request.user)
#         category = Category.objects.get(id=category_id)
#
#         if role == "seller":
#             product = Product(
#                 seller=seller_or_trader,
#                 name=name,
#                 price=price,
#                 description=description,
#                 image=image,
#                 stock=stock,
#                 category=category
#             )
#         elif role == "trader":
#             product = Product(
#                 trader=seller_or_trader,  # Assuming Product has a "trader" field
#                 name=name,
#                 price=price,
#                 description=description,
#                 image=image,
#                 stock=stock,
#                 category=category
#             )
#         else:
#             logger.error("Invalid role.")
#             return HttpResponse("Invalid role.", status=400)
#
#         product.save()
#         logger.info("Product saved successfully.")
#         return redirect(redirect_url)
#
#     categories = Category.objects.all()
#     return render(request, "add_product.html", {
#         "categories": categories,
#         "role": role,
#         "action_url": redirect_url,
#         "profile_url": f"{role}_profile",
#     })
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class SellerViewSet(viewsets.ModelViewSet):
#     queryset = Seller.objects.all()
#     serializer_class = SellerSerializer
#
#
# @login_required
# def seller_profile(request):
#     user = request.user
#     if request.method == "POST":
#         user.first_name = request.POST.get("first_name", user.first_name)
#         user.last_name = request.POST.get("last_name", user.last_name)
#         user.email = request.POST.get("email", user.email)
#
#         if "profile_picture" in request.FILES:
#             user.profile_picture = request.FILES["profile_picture"]
#
#         user.save()
#
#         # Update the seller's stores
#         if request.user.role == 'seller':
#             seller, created = Seller.objects.get_or_create(user=user)
#             store_ids = request.POST.getlist("stores")
#             stores = Store.objects.filter(id__in=store_ids)
#             seller.stores.set(stores)
#             seller.save()
#
#         return redirect("seller_profile")
#
#     stores = Store.objects.all()
#     return render(request, "seller_profile.html", {"stores": stores})
#
#
# def seller_add_product(request):
#     return product_creation(request, 'seller', Seller, 'seller_products')
#
#
# @login_required
# def seller_products(request):
#     if request.user.role != 'seller':
#         return HttpResponse("You are not registered as a seller.", status=403)
#
#     seller, _ = Seller.objects.get_or_create(user=request.user)  # Получаем или создаем Seller
#     products = Product.objects.filter(seller=seller)
#
#     return render(request, "seller_feed.html", {"products": products})
#
#
# class TraderViewSet(viewsets.ModelViewSet):
#     queryset = Trader.objects.all()
#     serializer_class = TraderSerializer
#
#
# @login_required
# @user_passes_test(lambda user: user.role == "trader")
# def trader_profile(request):
#     if request.method == "POST":
#         user = request.user
#         user.first_name = request.POST.get("first_name", user.first_name)
#         user.last_name = request.POST.get("last_name", user.last_name)
#         user.email = request.POST.get("email", user.email)
#         user.role = request.POST.get("role", user.role)
#
#         if "profile_picture" in request.FILES:
#             user.profile_picture = request.FILES["profile_picture"]
#
#         user.save()
#         return redirect("trader_profile")  # Перенаправляет обратно после сохранения
#
#     return render(request, "trader_profile.html")
#
#
# def trader_add_product(request):
#     return product_creation(request, 'trader', Trader, 'trader_products')
#
#
# @login_required
# def trader_products(request):
#     if request.user.role != 'trader':
#         return HttpResponse("You are not registered as a trader.", status=403)
#
#     trader, _ = Trader.objects.get_or_create(user=request.user)  # Получаем или создаем Seller
#     products = Product.objects.filter(trader=trader)
#
#     return render(request, "trader_feed.html", {"products": products})
#
#
# @login_required
# @user_passes_test(lambda user: user.role == "admin")
# def admin_profile(request):
#     users = User.objects.all().order_by("-role")
#     return render(request, "admin_page.html", {"users": users})
#
#
# @login_required
# @user_passes_test(lambda user: user.role == "customer")
# def customer_profile(request):
#     user = request.user  # Получаем текущего пользователя
#
#     if request.method == "POST":
#         user.first_name = request.POST.get("first_name", user.first_name)
#         user.last_name = request.POST.get("last_name", user.last_name)
#         user.email = request.POST.get("email", user.email)
#
#         if "profile_picture" in request.FILES:
#             user.profile_picture = request.FILES["profile_picture"]  # Загружаем файл
#
#         user.save()
#         return redirect("customer_profile")  # Обновление страницы
#
#     return render(request, "customer_profile.html")
#
#
# def customer_feed(request):
#     return render(request, 'customer_feed.html')
#
#
# def customer_requests(request):
#     return render(request, 'customer_request.html')
#
#
# def purchase_history(request):
#     return render(request, 'purchase_history.html')



# <h2>All Products</h2>
#
# {% if products %}
#     <ul>
#         {% for product in products %}
#             <li>
#                 <strong>{{ product.name }}</strong> - ${{ product.price }}
#                 <p>{{ product.description }}</p>
#                 {% if product.image %}
#                     <img src="{{ product.image.url }}" alt="{{ product.name }}" width="150">
#                 {% endif %}
#             </li>
#         {% endfor %}
#     </ul>
# {% else %}
#     <p>No products added yet.</p>
# {% endif %}
#
# <a href="{% url 'trader_profile' %}">Back to Profile</a>
#

#
# <!--<h2>My Purchase Requests</h2>-->
# <!--<table>-->
# <!--    <tr>-->
# <!--        <th>Product</th>-->
# <!--        <th>Status</th>-->
# <!--    </tr>-->
# <!--    {% for request in my_purchase_requests %}-->
# <!--    <tr>-->
# <!--        <td>{{ request.product.name }}</td>-->
# <!--        <td>{{ request.status }}</td>-->
# <!--    </tr>-->
# <!--    {% empty %}-->
# <!--    <tr><td colspan="2">No purchase requests found.</td></tr>-->
# <!--    {% endfor %}-->
# <!--</table>-->
# <h2>Purchase Requests (Requests from Customers)</h2>
# <table>
#     <tr>
#         <th>Product</th>
#         <th>Customer</th>
#         <th>Status</th>
#         <th>Actions</th>
#     </tr>
#     {% for request in incoming_requests %}
#     <tr>
#         <td>{{ request.product.name }}</td>
#         <td>{{ request.customer.user.username }}</td>
#         <td>{{ request.status }}</td>
#         <td>
#             <a href="{% url 'trader_accept_request' request.id %}">Accept</a> |
#             <a href="{% url 'trader_deny_request' request.id %}">Deny</a>
#         </td>
#     </tr>
#     {% empty %}
#     <tr><td colspan="4">No incoming requests found.</td></tr>
#     {% endfor %}
# </table>

# <!--    <tr><td colspan="2">No purchase requests found.</td></tr>-->


