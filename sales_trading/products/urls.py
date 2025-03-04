from django.urls import path
from .views import ProductFeedView

urlpatterns = [
    path('', ProductFeedView.as_view(), name='product-list'),
    path('<int:pk>/', ProductFeedView.as_view(), name='product-detail'),

]