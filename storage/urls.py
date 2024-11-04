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
    path('search/', views.search, name='storage-search'),
    path('search/autopart', views.search_autopart, name='storage-search-autopart'),
    path('search/location', views.search_location, name='storage-search-location'),
    path('search/stock', views.search_stock, name='storage-search-stock'),
]
