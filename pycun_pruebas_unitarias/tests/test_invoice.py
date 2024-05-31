import pytest
from decimal import Decimal

from django.urls import reverse
from django.test import Client

from pycun_pruebas_unitarias.apps.invoice.views import is_greater_than, sum
from pycun_pruebas_unitarias.apps.invoice.models import Invoice, InvoiceArticle
from pycun_pruebas_unitarias.apps.invoice.utils import calculate_taxes_per_item


def test_sum():
    assert sum(2, 5) == 7


def test_is_greater_than():
    assert is_greater_than(10, 2)


@pytest.mark.parametrize(
    "input_x, input_y, expected",
    [
        (5, 1, 6),
        (6, sum(4, 2), 12),
        (sum(19, 1), 15, 35),
        (-7, 10, sum(-7, 10))
    ]
)
def test_sum_params(input_x, input_y, expected):
    assert sum(input_x, input_y) == expected


@pytest.mark.parametrize(
    "quantity, price, tax_percentage, expected_result",
    [
        (Decimal(1), Decimal(100), Decimal(16), {
            "sub_total": Decimal(100),
            "total_tax": Decimal(16),
            "total_before_tax": Decimal(100),
            "total_after_taxes": Decimal(116)
        }),
        (Decimal(1), Decimal(100), Decimal(19), {
            "sub_total": Decimal(100),
            "total_tax": Decimal(19),
            "total_before_tax": Decimal(100),
            "total_after_taxes": Decimal(119)
        }),
        (Decimal(2), Decimal(100), Decimal(19), {
            "sub_total": Decimal(200),
            "total_tax": Decimal(38),
            "total_before_tax": Decimal(200),
            "total_after_taxes": Decimal(238)
        })
    ]   
)
def test_taxes_per_article(quantity, price, tax_percentage, expected_result):

    result = calculate_taxes_per_item(quantity, price, tax_percentage)

    # Verificar que el resultado sea un diccionario
    assert isinstance(result, dict), "El resultado debe ser un diccionario"

    # Verificar que el diccionario contiene las claves y valores esperados
    assert result == expected_result, "El contenido del diccionario no es el esperado"


@pytest.mark.django_db
def test_invoice_create_view():
    client = Client()

    # Datos del formulario para la factura
    invoice_data = {
        'invoice-tax': '10',  # Suponiendo que el impuesto es del 10%
    }

    # Datos del formset para los artículos de la factura
    article_data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MIN_NUM_FORMS': '0',
        'form-MAX_NUM_FORMS': '1000',
        'form-0-quantity': '2',
        'form-0-description': 'Artículo de prueba',
        'form-0-price': '100.00',
    }

    # Combina los datos del formulario de factura y los artículos
    post_data = {**invoice_data, **article_data}

    # Realiza la solicitud POST
    response = client.post(reverse('invoice_create'), data=post_data)

    # Comprueba que la respuesta redirige a la vista de lista de facturas
    assert response.status_code == 302
    assert response.url == reverse('invoice_list')

    # Verifica que la factura se ha creado en la base de datos
    # assert Invoice.objects.count() == 1
    invoice = Invoice.objects.last()
    assert invoice.tax == 10
    assert invoice.sub_total == 200  # 2 * 100.00
    assert invoice.total_tax == 20   # 200 * 0.10
    assert invoice.total == 220      # 200 + 20

    # Verifica que el artículo de la factura se ha creado en la base de datos
    # assert InvoiceArticle.objects.count() == 1
    article = InvoiceArticle.objects.last()
    assert article.quantity == 2
    assert article.description == 'Artículo de prueba'
    assert article.price == 100.00
    assert article.invoice == invoice
