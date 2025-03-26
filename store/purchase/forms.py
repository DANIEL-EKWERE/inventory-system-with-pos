from django import forms
from .models import Supplier, PurchaseProduct
from inventory.models import *

from django.core.exceptions import ValidationError
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_info']
        labels = {
            'name': 'Full Name (Person/Company)',
            'contact_info': 'Supplier Information',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name / Company Ltd.    ',
            }),
            'contact_info': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Information:\n Address\n Phone\n Business Type\n Etc',
                'rows': 6,  
            }),
        }
        error_messages = {
            'name': {
                'required': 'Supplier name is required.',
                'max_length': 'Name cannot exceed 100 characters.',
            },
            'contact_info': {
                'required': 'Contact information is required.',
                'max_length': 'Contact information cannot exceed 200 characters.',
            },
        }

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = PurchaseProduct
        fields = ['supplier', 'product','cost','qty']
        labels = {
            'supplier': 'Supplier',
            'product': 'Products',
            'cost': 'Cost',
            'qty': 'Quantity',
        }
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter total amount',
            }),
            'qty': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter total amount',
            }),
        }
        error_messages = {
            'qty': {
               'required': 'Quantity is required.',
                'invalid': 'Enter a valid quantity.',
            },
            'cost':{
                'required': 'Cost must have 8 decimal places.',
                'invalid': 'Enter a valid amount.',
            }
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Ordenar el queryset de category alfabéticamente
        self.fields['supplier'].queryset = Supplier.objects.all().order_by('name')
        self.fields['product'].queryset = Products.objects.all().order_by('name')
    
