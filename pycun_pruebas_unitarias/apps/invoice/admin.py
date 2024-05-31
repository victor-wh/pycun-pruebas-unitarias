# django packages
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# local packages
from pycun_pruebas_unitarias.apps.invoice.models import Invoice, InvoiceArticle


# Register your models here.
# admin.site.register(Factura, UserAdmin)
class InvoiceArticleInLine(admin.TabularInline):
    model = InvoiceArticle
    raw_id_fields = ['invoice']
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'total', 'sub_total', 'tax')
    search_fields =('id', 'total', 'sub_total', 'tax')
    inlines = [
        InvoiceArticleInLine
    ]


@admin.register(InvoiceArticle)
class InvoiceArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'quantity', 'description')
    list_select_related = ('invoice',)
    raw_id_fields = list_select_related
    search_fields = ('id',)
