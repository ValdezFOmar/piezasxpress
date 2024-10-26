from django.urls import path

from core.views import simple_view

urlpatterns = [
    path('', simple_view('orders/search-order.html'), name='orders-search-order'),
]
