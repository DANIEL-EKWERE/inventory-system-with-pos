from datetime import datetime
from unicodedata import category
from django.db import models
from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from inventory.models import *


class Creditor(models.Model):
    sale_id = models.CharField(max_length=100,default="")
    customer = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    amount = models.FloatField(default=0)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    paid_amount = models.FloatField(default=0)
    balance = models.FloatField(default=0)

    def __str__(self):
        return self.customer

class Sales(models.Model):
    code = models.CharField(max_length=100)
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    tendered_amount = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 
 
    cliente = models.CharField(max_length=100, blank=True)  

    def save(self, *args, **kwargs):
        if not self.pk or self.cliente == "Customer 1": 
            
            ventas_hoy = Sales.objects.filter(date_added__date=timezone.now().date()).count()
            
            self.cliente = f"Customer {ventas_hoy + 1}"
            print("Customer:", self.cliente) 
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.code

        
class salesItems(models.Model):
    
    sale = models.ForeignKey(Sales,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    qty = models.IntegerField(default=0)
    total = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        print(f"Saving SalesItem: Product: {self.product.name}, Quantity Sold: {self.qty}")
        super().save(*args, **kwargs)
        self.update_product_quantity()
        

    def update_product_quantity(self):
        self.product.update_quantity_on_sale(self.qty)
    
    
    def delete(self, *args, **kwargs):
        print(f"Deleting SalesItem: Product: {self.product.name}, Quantity Sold: {self.qty}")
        self.product.increase_quantity(self.qty)
        super().delete(*args, **kwargs)