from django import forms


class QuotationForm(forms.Form):
    client = forms.CharField(max_length=100)
