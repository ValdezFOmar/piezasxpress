import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from core.models import CarPart

from .forms import QuotationForm
from .models import Bill, Quotation, QuotationPart


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
    return render(request, 'orders/quotation.html', context)


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


def bill_from_quote(request: HttpRequest, id: int) -> HttpResponse:
    quotation = get_object_or_404(Quotation, id=id)
    has_bill = hasattr(quotation, 'bill')
    price = sum(p.price for p in quotation.parts.all())

    if request.method == 'POST':
        if not has_bill:
            Bill.objects.create(quotation=quotation, date=timezone.now(), payment=price)
        return redirect('home')

    context = {'quotation': quotation, 'total_price': price, 'has_bill': has_bill}
    return render(request, 'orders/bill.html', context)
