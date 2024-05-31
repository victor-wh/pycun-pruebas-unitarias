from django.forms import modelformset_factory
from django.shortcuts import render, redirect

from pycun_pruebas_unitarias.apps.invoice.utils import calculate_taxes_per_item

from pycun_pruebas_unitarias.apps.invoice.models import Invoice, InvoiceArticle

from pycun_pruebas_unitarias.apps.invoice.forms.invoice_forms import InvoiceForm, InvoiceArticleForm


# region funciones basicas
def sum(x, y):
    return x + y


def is_greater_than(number_1, number_2):
    return number_1 > number_2
# endregion funciones

# region Invoice
def home(request):
    return render(request, 'home.html')

def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, "invoice_list.html", {
        "invoices": invoices,
    })


def invoice_create(request):
    invoice_article_formset = modelformset_factory(InvoiceArticle, form=InvoiceArticleForm, extra=1)
    if request.method == "POST":
        invoice_form = InvoiceForm(request.POST, prefix='invoice')
        formset = invoice_article_formset(request.POST)
        if formset.is_valid() and invoice_form.is_valid():
            articles = formset.save(commit=False)
            invoice = invoice_form.save(commit=False)
            invoice.total = 0
            invoice.sub_total = 0
            invoice.total_tax = 0
            invoice.save()

            taxes = invoice_form.cleaned_data.get('tax')
            
            for article in articles:
                data_taxes = calculate_taxes_per_item(quantity=article.quantity, price=article.price, tax_percentage=taxes)
                invoice.sub_total += data_taxes.get('sub_total')
                invoice.total_tax += data_taxes.get('total_tax')
                invoice.total += data_taxes.get('total_after_taxes')
                article.invoice = invoice
                article.save()
                print(f"Article: {article.id}, Sub Total: {invoice.sub_total}, Total Tax: {invoice.total_tax}, Total: {invoice.total}")
            invoice.save()
            return redirect('invoice_list')
    else:
        invoice_form = InvoiceForm(prefix='invoice')
        formset = invoice_article_formset(queryset=InvoiceArticle.objects.none())

    return render(request, 'invoice_create.html', {'invoice_form': invoice_form, 'formset': formset})
# endregion Invoice
