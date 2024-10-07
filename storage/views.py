import json
from collections.abc import Callable
from typing import NamedTuple
from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render

from core.models import Car, Part

from .forms import CarModelForm


class PartDefinition(NamedTuple):
    id: int
    name: str
    location: str


def simple_view(template_name: str) -> Callable[[HttpRequest], HttpResponse]:
    return login_required(lambda request: render(request, template_name))


@login_required
def add_car(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CarModelForm(request.POST)
        if form.is_valid():
            car: Car = form.save(commit=True)
            return redirect('storage-add-part', car_id=car.id)
    else:
        form = CarModelForm()
    return render(request, 'storage/add.html', {'form': form})


def add_car_parts(request: HttpRequest, car_id: int) -> HttpResponse:
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        # TODO: Add code to assosiate parts with the car
        pass
    else:
        pass

    return render(request, 'storage/add-part.html', {'car': car})


def register_part(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponseBadRequest()

    parts: list[PartDefinition] = json.loads(
        request.body, object_hook=lambda attrs: PartDefinition(**attrs)
    )

    Part.objects.bulk_create(
        Part(part_id=part.id, name=part.name, location=part.location) for part in parts
    )

    return HttpResponse(status=HTTPStatus.NO_CONTENT)


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
