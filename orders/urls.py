from django.urls import path

from core.views import simple_view
from .views import add_parts, quotation_form

urlpatterns = [
    path('', simple_view('orders/search-order.html'), name='orders-search-order'),
    path('add-parts', add_parts, name='orders-add-parts'),
    path('quotation', quotation_form, name='orders-quotation-form')
]
