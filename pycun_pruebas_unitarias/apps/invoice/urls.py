from django.conf.urls import url
from django.urls import path

from pycun_pruebas_unitarias.apps.invoice.views import invoice_list, invoice_create

urlpatterns = [
    path("invoice/list/", invoice_list, name="invoice_list"),
    path("invoice/create/", invoice_create, name="invoice_create")
]
