from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('users/login', views.login_user, name='user-login'),
    path('users/logout', views.logout_user, name='user-logout'),
    path('search', views.search, name='search')
]
