from django.urls import path

from . import views
from .views import simple_view

urlpatterns = [
    path('', simple_view('storage/index.html'), name='storage-index'),
    path('add', simple_view('storage/add.html'), name='storage-add'),
    path('add-part', simple_view('storage/add-part.html'), name='storage-add-part'),
    path('search', simple_view('storage/search.html'), name='storage-search'),
    path('search/autopart', simple_view('storage/search-autopart.html'), name='storage-search-autopart'),
    path('search/autopart/results', views.search_autopart_results, name='storage-search-autopart-results'),
    path('search/location', simple_view('storage/search-location.html'), name='storage-search-location'),
    path('search/location/results', views.search_location_results, name='storage-search-location-results'),
    path('search/stock', simple_view('storage/search-stock.html'), name='storage-search-stock'),
    path('search/stock/results', views.search_stock_results, name='storage-search-stock-results'),
]
