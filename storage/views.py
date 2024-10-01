from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'storage/index.html')


@login_required
def add(request: HttpRequest) -> HttpResponse:
    return render(request, 'storage/add.html')


@login_required
def add_part(request: HttpRequest) -> HttpResponse:
    return render(request, 'storage/add-part.html')


@login_required
def search(request: HttpRequest) -> HttpResponse:
    return render(request, 'storage/search.html')


@login_required
def search_autopart(request: HttpRequest) -> HttpResponse:
    return render(request, 'storage/search-autopart.html')


@login_required
def search_location(request: HttpRequest) -> HttpResponse:
    return render(request, 'storage/search-location.html')


@login_required
def search_stock(request: HttpRequest) -> HttpResponse:
    return render(request, 'storage/search-stock.html')
