from __future__ import annotations

import json
from decimal import Decimal
from http import HTTPStatus
from typing import Any, NamedTuple, TypedDict

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from core.models import Car, Part
from core.models import CarPart as CarPartModel

from .forms import CarModelForm, SearchStockForm


class PartDefinition(NamedTuple):
    id: int
    name: str


class CarPart(TypedDict):
    partId: int
    name: str
    price: Decimal
    quantity: int
    comment: str


@login_required
def search(_: HttpRequest) -> HttpResponse:
    return redirect('storage-search-autopart')


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


@login_required
def add_car_parts(request: HttpRequest, car_id: int) -> HttpResponse:
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'GET':
        return render(request, 'storage/add-part.html', {'car': car})
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST', 'GET'])

    try:
        parts: list[CarPart] = json.loads(
            request.body, parse_float=Decimal
        )
    except json.JSONDecodeError as e:
        return HttpResponseBadRequest(content=e.msg)

    car_parts = [
        CarPartModel(
            car=car,
            part=Part.objects.get(part_id=part['partId']),
            price=part['price'],
            quantity=part['quantity'],
            comment=part['comment'],
        )
        for part in parts
    ]

    CarPartModel.objects.bulk_create(car_parts)

    return redirect('storage-index')


@csrf_exempt
def register_part(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    parts: list[PartDefinition] = json.loads(
        request.body, object_hook=lambda attrs: PartDefinition(**attrs)
    )

    Part.objects.bulk_create(Part(part_id=part.id, name=part.name) for part in parts)

    return HttpResponse(status=HTTPStatus.NO_CONTENT)


def parts_list(request: HttpRequest) -> HttpResponse:
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    parts = [{'id': p.part_id, 'name': p.name} for p in Part.objects.all()]
    content = json.dumps(parts)
    return HttpResponse(content)


# TODO: Actually implement the search features
@login_required
def search_autopart(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        pass
    else:
        pass
    return render(request, 'storage/search-autopart.html')


@login_required
def search_location(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        pass
    else:
        pass
    return render(request, 'storage/search-location.html')


@login_required
def search_stock(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SearchStockForm(request.POST)
        if form.is_valid():
            stock = form.cleaned_data['stock']
            parts = CarPartModel.objects.filter(car__stock=stock, )
            return render(request, 'storage/results.html', {'parts': parts})
    else:
        form = SearchStockForm()
    return render(request, 'storage/search-stock.html', {'form': form})
