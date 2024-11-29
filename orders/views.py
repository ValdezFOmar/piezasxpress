import json
from typing import TYPE_CHECKING, TypeVar

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from core.models import CarPart

from .forms import QuotationForm, SearchOrderForm
from .models import Bill, Quotation, QuotationPart

if TYPE_CHECKING:
    from django.db.models import Model


def get_or_none[T: Model](model: type[T], **kwargs: object) -> T | None:
    try:
        return model.objects.get(**kwargs)
    except (model.DoesNotExist, model.MultipleObjectsReturned):
        return None


@login_required
def search_order_form(request: HttpRequest) -> HttpResponse:
    return render(request, 'orders/search-order.html')


@login_required
def search_order(request: HttpRequest) -> HttpResponse:
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    form = SearchOrderForm(request.GET)
    if not form.is_valid():
        return redirect('orders-search-order')

    order_type = form.cleaned_data['order_type']
    order_id = form.cleaned_data['order_id']
    client_name = form.cleaned_data['client_name']

    if order_type == SearchOrderForm.Order.BILL:
        bill = get_or_none(Bill, id=order_id, quotation__client_name=client_name)
        if bill is None:
            return render(request, 'orders/no-results.html')
        return render(request, 'orders/bill.html', {'bill': bill})

    if order_type == SearchOrderForm.Order.QUOTATION:
        quotation = get_or_none(Quotation, id=order_id, client_name=client_name)
        if quotation is None:
            return render(request, 'orders/no-results.html')
        price = sum(part.price for part in quotation.parts.all())
        context = {'quotation': quotation, 'total_price': price}
        return render(request, 'orders/quotation.html', context)

    return HttpResponseBadRequest('order must be one of "bill" or "quotation"')


@login_required
def quotation_form(request: HttpRequest) -> HttpResponse:
    if 'parts' not in request.session:
        return redirect('home')
    part_ids = request.session['parts']
    date = timezone.now()
    parts = CarPart.objects.filter(id__in=part_ids).order_by('part__part_id')
    price = sum(p.price for p in parts)
    context = {
        'date': date,
        'parts': parts,
        'total_price': price,
    }
    return render(request, 'orders/quotation-form.html', context)


@login_required
def save_quotation(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    form = QuotationForm(request.POST)
    if not form.is_valid():
        return redirect('orders-quotation-form')
    if 'parts' not in request.session:
        return redirect('home')

    client = form.cleaned_data['client']
    part_ids = request.session['parts']
    parts = CarPart.objects.filter(id__in=part_ids)
    quotation = Quotation.objects.create(
        client_name=client,
        date=timezone.now(),
        user=request.user.username,  # pyright: ignore[reportAttributeAccessIssue]
    )

    QuotationPart.objects.bulk_create(
        QuotationPart(car_part=part, quotation=quotation) for part in parts
    )

    if request.POST.get('make') == 'bill':
        return redirect('orders-create-bill', id=quotation.id)
    else:
        return redirect('home')


@login_required
def add_parts(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    try:
        parts: list[int] = json.loads(request.body)
    except json.JSONDecodeError as error:
        return HttpResponseBadRequest(content=error.msg)

    request.session['parts'] = parts
    print(request.session['parts'])

    return redirect('orders-quotation-form')


@login_required
def bill_from_quote(request: HttpRequest, id: int) -> HttpResponse:
    quotation = get_object_or_404(Quotation, id=id)
    has_bill = hasattr(quotation, 'bill')
    price = sum(p.price for p in quotation.parts.all())

    if request.method == 'POST':
        if not has_bill:
            Bill.objects.create(quotation=quotation, date=timezone.now(), payment=price)
        return redirect('home')

    context = {
        'quotation': quotation,
        'total_price': price,
        'has_bill': has_bill,
    }
    return render(request, 'orders/bill-form.html', context)
