from django.db import models

from core.models import Part, validate_positive


class Client(models.Model):
    first_names = models.CharField(max_length=50)
    last_names = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.first_names} {self.last_names}'


class Quotation(models.Model):
    parts = models.ManyToManyField(Part, through='QuotationPart')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField()


class QuotationPart(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[validate_positive])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['quotation', 'part'], name='unique_quotation'),
        ]


class Bill(models.Model):
    date = models.DateTimeField()
    payment = models.DecimalField(max_digits=7, decimal_places=2, validators=[validate_positive])
    quotation = models.OneToOneField(Quotation, on_delete=models.CASCADE)
