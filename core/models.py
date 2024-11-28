from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def validate_range(value: int, min: int, max: int):
    if not (min <= value <= max):
        raise ValidationError(f'Expected a value in the range [{min}, {max}], got {value}')


def validate_car_year(value: int):
    validate_range(value, 1900, timezone.now().year)


def validate_positive(value: int):
    if value < 0:
        raise ValidationError(f'Expected a positive value, got {value!r}')


def validate_not_empty(value: str):
    if value == '':
        raise ValidationError('Value must not be the empty string')


class Part(models.Model):
    # ID given when registering the part, not the actual database ID
    part_id = models.IntegerField(unique=True, validators=[validate_positive])
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Car(models.Model):
    class Transmission(models.TextChoices):
        AUTOMATIC = 'A'
        MANUAL = 'M'

    class Traction(models.TextChoices):
        AWD = 'AWD', 'AWD'
        FWD = 'FWD', 'FWD'
        RWD = 'RWD', 'RWD'
        _4X4 = '4X4', '4X4'

    # Type hinting
    id: models.BigAutoField

    miles = models.IntegerField(validators=[validate_positive])
    model = models.CharField(max_length=50)
    motor = models.CharField(max_length=50)
    parts = models.ManyToManyField(Part, through='CarPart')
    stock = models.CharField(max_length=10, unique=True, validators=[validate_not_empty])
    traction = models.CharField(max_length=3, choices=Traction.choices)
    transmisson = models.CharField(max_length=1, choices=Transmission.choices)
    year = models.IntegerField(validators=[validate_car_year])

    def __str__(self) -> str:
        return f'{self.model} ({self.year}) <stock:{self.stock}>'


class CarPart(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    location = models.CharField(max_length=10, null=True, validators=[validate_not_empty])
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[validate_positive])
    quantity = models.IntegerField(default=0, validators=[validate_positive])
    comment = models.TextField(default='')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['car', 'part'], name='unique_car_part')]

    def __str__(self) -> str:
        return f'{self.part.name} <stock:{self.car.stock}>'
