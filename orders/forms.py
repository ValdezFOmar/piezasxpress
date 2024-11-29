from django import forms
from django.db.models import TextChoices


class SearchOrderForm(forms.Form):
    class Order(TextChoices):
        BILL = 'bill', 'Factura'
        QUOTATION = 'quotation', 'Cotización'

    order_type = forms.ChoiceField(choices=Order.choices)
    order_id = forms.IntegerField()
    client_name = forms.CharField()


class QuotationForm(forms.Form):
    client = forms.CharField(max_length=100)
