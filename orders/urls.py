from django.urls import path

from core.views import simple_view
from . import views

urlpatterns = [
    path('', simple_view('orders/search-order.html'), name='orders-search-order'),
    path('add-parts', views.add_parts, name='orders-add-parts'),
    path('quotation', views.quotation_form, name='orders-quotation-form'),
    path('quotation/save', views.save_quotation, name='orders-save-quotation'),
    path('quotation/<int:id>/create-bill', views.bill_from_quote, name='orders-create-bill'),
]
