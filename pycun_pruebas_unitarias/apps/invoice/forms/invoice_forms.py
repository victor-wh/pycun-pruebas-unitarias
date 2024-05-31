# forms.py
from django import forms

from pycun_pruebas_unitarias.apps.invoice.models import Invoice, InvoiceArticle


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['tax', ]


class InvoiceArticleForm(forms.ModelForm):
    class Meta:
        model = InvoiceArticle
        fields = ['quantity', 'description', 'price', ]
