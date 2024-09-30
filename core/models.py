from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def validate_range(value: int, min: int, max: int):
    if not (min <= value <= max):
        raise ValidationError(f'Expected a value in the range [{min}, {max}], got {value}')


def validate_car_year(value: int):
    validate_range(value, 1950, timezone.now().year)


def validate_positive(value: int):
    if value < 0:
        raise ValidationError(f'Expected a positive value, got {value!r}')


def validate_not_empty(value: str):
    if value == '':
        raise ValidationError('Value must not be the empty string')


class Motor(models.Model):
    type = models.CharField(max_length=4)


class Traction(models.Model):
    type = models.CharField(max_length=3)


class Part(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[validate_positive])
    location = models.CharField(max_length=10, validators=[validate_not_empty])
    quantity = models.IntegerField(validators=[validate_positive])

    def __str__(self) -> str:
        return self.name


class Car(models.Model):
    class Transmission(models.TextChoices):
        AUTOMATIC = 'a'
        MANUAL = 'm'

    model = models.CharField(max_length=50)
    year = models.IntegerField(validators=[validate_car_year])
    transmisson = models.CharField(max_length=1, choices=Transmission.choices)
    motor = models.ForeignKey(Motor, on_delete=models.CASCADE)
    traction = models.ForeignKey(Traction, on_delete=models.CASCADE)
    parts = models.ManyToManyField(Part)

    def __str__(self) -> str:
        return f'{self.model} ({self.year})'
