from django import forms

from core.models import Car, validate_not_empty


class SearchAutoPartForm(forms.Form):
    year = forms.IntegerField(
        error_messages={
            'invalid': 'Por favor, introduce un número válido para el año.',
        }
    )
    model = forms.CharField()
    part_id = forms.IntegerField()


class SearchLocationForm(forms.Form):
    part_id = forms.IntegerField()
    location = forms.CharField()


class SearchStockForm(forms.Form):
    stock = forms.CharField(validators=[validate_not_empty])


class CarModelForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'miles',
            'model',
            'motor',
            'stock',
            'traction',
            'transmisson',
            'year',
        ]

        widgets = {
            'miles': forms.NumberInput(attrs=dict(min=0, value=0)),
            'motor': forms.TextInput(attrs=dict(max=50, spellcheck='false')),
            'stock': forms.TextInput(attrs=dict(max=10, spellcheck='false')),
            'year': forms.NumberInput(attrs=dict(min=1900, max=2099, step=1)),
        }
