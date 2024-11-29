from django.urls import path

from . import views

urlpatterns = [
    path('search', views.search_order_form, name='orders-search-order'),
    path('search/results', views.search_order, name='orders-search-order-results'),
    path('add-parts', views.add_parts, name='orders-add-parts'),
    path('quotation', views.quotation_form, name='orders-quotation-form'),
    path('quotation/save', views.save_quotation, name='orders-save-quotation'),
    path('quotation/<int:id>/create-bill', views.bill_from_quote, name='orders-create-bill'),
]
