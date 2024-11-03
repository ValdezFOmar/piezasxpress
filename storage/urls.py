from django.urls import path

from core.views import simple_view

from . import views

urlpatterns = [
    path('', simple_view('storage/index.html'), name='storage-index'),
    path('car/add', views.add_car, name='storage-add'),
    path('car/<int:car_id>/parts', views.add_car_parts, name='storage-add-part'),
    # Use to populate the parts catalog with json encoded data
    path('part/register', views.register_part, name='storage-register-part'),
    path('part/list', views.parts_list, name='storage-list-parts'),
    path('search', simple_view('storage/search.html'), name='storage-search'),
    path(
        'search/autopart',
        simple_view('storage/search-autopart.html'),
        name='storage-search-autopart',
    ),
    path(
        'search/autopart/results',
        views.search_autopart_results,
        name='storage-search-autopart-results',
    ),
    path(
        'search/location',
        simple_view('storage/search-location.html'),
        name='storage-search-location',
    ),
    path(
        'search/location/results',
        views.search_location_results,
        name='storage-search-location-results',
    ),
    path('search/stock', simple_view('storage/search-stock.html'), name='storage-search-stock'),
    path('search/stock/results', views.search_stock_results, name='storage-search-stock-results'),
]
