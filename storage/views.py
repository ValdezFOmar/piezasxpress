from collections.abc import Callable

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def simple_view(template_name: str) -> Callable[[HttpRequest], HttpResponse]:
    @login_required
    def inner(request: HttpRequest) -> HttpResponse:
        return render(request, template_name)

    return inner


# TODO: Actually implement the search features
@login_required
def search_autopart_results(request: HttpRequest) -> HttpResponse:
    return render(request, 'storage/results.html')


@login_required
def search_location_results(request: HttpRequest) -> HttpResponse:
    return render(request, 'storage/results.html')


@login_required
def search_stock_results(request: HttpRequest) -> HttpResponse:
    return render(request, 'storage/results.html')
