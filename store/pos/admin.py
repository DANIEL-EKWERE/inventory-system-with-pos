from django.contrib import admin
from .models import Sales, salesItems, Creditor

class SalesAdmin(admin.ModelAdmin):
    list_display = ('code', 'sub_total', 'grand_total', 'tax_amount', 'tax', 'tendered_amount', 'amount_change', 'date_added', 'date_updated', 'cliente')
    search_fields = ('code', 'cliente')
    list_filter = ('date_added', 'date_updated')

class SalesItemsAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'price', 'qty', 'total')
    search_fields = ('sale__code', 'product__name')
    list_filter = ('sale__date_added',)

class CreditorAdmin(admin.ModelAdmin):
    list_display = ('sale_id','customer', 'phone', 'email', 'address', 'date_added', 'date_updated', 'amount', 'paid_amount', 'balance')
    search_fields = ('sale_id','customer', 'phone', 'email', 'address')
    list_filter = ('date_added', 'date_updated')


admin.site.register(Sales, SalesAdmin)
admin.site.register(Creditor, CreditorAdmin)
admin.site.register(salesItems, SalesItemsAdmin)
