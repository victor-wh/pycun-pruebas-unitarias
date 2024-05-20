from django.db import models


class Invoice(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):
        return f'{self.id}'


class InvoiceArticle(models.Model):
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    invoice = models.ForeignKey(Invoice, related_name='invoice_articles', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}'

