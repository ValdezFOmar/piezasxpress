from django.db import models

from core.models import CarPart, validate_positive


class Quotation(models.Model):
    id: models.BigAutoField  # type hinting

    client_name = models.CharField(max_length=100)
    date = models.DateField()
    parts = models.ManyToManyField(CarPart, through='QuotationPart')
    user = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'For {self.client_name} by {self.user} <id:{self.id}>'


class QuotationPart(models.Model):
    car_part = models.ForeignKey(CarPart, on_delete=models.CASCADE)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['quotation', 'car_part'], name='unique_quotation_part')
        ]

    def __str__(self) -> str:
        return f'{self.car_part.part.name} <Quotation:{self.quotation.id}>'


class Bill(models.Model):
    id: models.BigAutoField  # type hinting

    quotation = models.OneToOneField(Quotation, on_delete=models.CASCADE)
    date = models.DateField()
    payment = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive])

    def __str__(self) -> str:
        return f'{self.quotation.client_name} ({self.date}) <id:{self.id}>'
