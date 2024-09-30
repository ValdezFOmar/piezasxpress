from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='storage-index'),
    path('add', views.add, name='storage-add'),
    path('add-part', views.add_part, name='storage-add-part'),
    path('search', views.search, name='storage-search'),
    path('search/autopart', views.search_autopart, name='storage-search-autopart'),
    path('search/location', views.search_location, name='storage-search-location'),
    path('search/stock', views.search_stock, name='storage-search-stock'),
]
