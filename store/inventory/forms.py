# from django import forms
# from .models import  Products, Category
# import unicodedata
# from django.utils.text import slugify
# import re
# import unicodedata
# from django.core.exceptions import ValidationError

# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['name', 'description']
#         labels = {
#             'name': 'Name',
#             'description': 'Description',
#         }
#         widgets = {
#             'name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Vino Dulce',
#             }),
#             'description': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Enter general information Etc.',
#                 'rows': 3,  
#             }),
            
#         }
#         error_messages = {
#             # Puedes agregar mensajes de error personalizados aquí si es necesario
#         }
        
#     def clean_name(self):
#         name = self.cleaned_data.get('name')
#         if name:
#             # Normalizar el nombre: eliminar acentos, espacios extra y convertir a minúsculas
#             normalized_name = ''.join(c for c in unicodedata.normalize('NFD', name)
#                                     if unicodedata.category(c) != 'Mn')
#             normalized_name = re.sub(r'\s+', '', normalized_name.lower())
            
#             instance = self.instance
#             # Buscar categorías existentes con nombres similares
#             existing_categories = Category.objects.exclude(id=instance.id)
#             for category in existing_categories:
#                 category_normalized = ''.join(c for c in unicodedata.normalize('NFD', category.name)
#                                             if unicodedata.category(c) != 'Mn')
#                 category_normalized = re.sub(r'\s+', '', category_normalized.lower())
#                 if category_normalized == normalized_name:
#                     raise ValidationError(f"Ya existe una categoría similar: '{category.name}'")
#         return name

        
# class ProductsForm(forms.ModelForm):
#     class Meta:
#         model = Products
#         fields = ['code', 'category', 'name', 'description', 'price', 'status']
#         labels = {
#             'code': 'Código',
#             'category': 'Categoría',
#             'name': 'Nombre del Producto',
#             'description': 'Descripción',
#             'price': 'Precio',
#             'status': 'Estado',
#             'cost': 'Costo',
#             'quantity': 'Cantidad',
#         }
#         widgets = {
#             'code': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Vino001',
#             }),
#             'category': forms.Select(attrs={
#                 'class': 'form-control',
#             }),
#             'name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Vino Dulce',
#             }),
#             'description': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Ingrese información general Etc.',
#                 'rows': 3,
#             }),
#             'price': forms.NumberInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Ingrese el precio del producto',
#                 'step': '0.01',
#             }),
#             'status': forms.Select(attrs={
#                 'class': 'form-control',
#             }, choices=[
#                 (1, 'Activo'),
#                 (0, 'Inactivo')
#             ]),
            
#             'cost': forms.NumberInput(attrs={
#                 'class': 'form-control'}),
#             'quantity': forms.NumberInput(attrs={
#                 'class': 'form-control'}),
#         }
#         error_messages = {
#             'code': {
#                 'required': 'Este campo es obligatorio.',
#                 'max_length': 'Este campo no puede exceder de 100 caracteres.',
#             },
#             'category': {
#                 'required': 'Este campo es obligatorio.',
#             },
#             'name': {
#                 'required': 'Este campo es obligatorio.',
#             },
#             'description': {
#                 'required': 'Este campo es obligatorio.',
#             },
#             'price': {
#                 'required': 'Este campo es obligatorio.',
#                 'invalid': 'Ingrese un precio válido.',
#             },
#             'status': {
#                 'required': 'Este campo es obligatorio.',
#                 'invalid': 'Ingrese un estado válido.',
#             }
#         }
#     def __init__(self, *args, **kwargs):
#         super(ProductForm, self).__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'
#             if field.errors:
#                 field.widget.attrs['class'] += ' is-invalid'
                
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
        
#         # Ordenar el queryset de category alfabéticamente
#         self.fields['category'].queryset = Category.objects.all().order_by('name')
#         # Establecer el campo como no editable
#         self.fields['status'].disabled = True
    
    
#     @staticmethod
#     def normalize_text(text):
#         if text:
#             # Eliminar acentos y convertir a minúsculas
#             text = ''.join(c for c in unicodedata.normalize('NFD', text)
#                         if unicodedata.category(c) != 'Mn')
#             # Eliminar caracteres especiales y espacios
#             text = re.sub(r'[^\w]', '', text.lower())
#         return text
    
#     def clean(self):
#         cleaned_data = super().clean()
#         name = cleaned_data.get('name')
#         code = cleaned_data.get('code')

#         if name and code:
#             normalized_name = self.normalize_text(name)
#             normalized_code = self.normalize_text(code)

#             # Obtener la instancia actual si estamos editando
#             instance_id = self.instance.pk if self.instance.pk else None

#             # Verificar duplicados de nombre
#             name_duplicates = Products.objects.all()
#             if instance_id:
#                 name_duplicates = name_duplicates.exclude(pk=instance_id)
            
#             for product in name_duplicates:
#                 if self.normalize_text(product.name) == normalized_name:
#                     self.add_error('name', "Ya existe un producto con un nombre similar.")
#                     raise ValidationError("Ya existe un producto con un nombre similar.")

#             # Verificar duplicados de código
#             code_duplicates = Products.objects.filter(code__iexact=normalized_code)
#             if instance_id:
#                 code_duplicates = code_duplicates.exclude(pk=instance_id)
#             if code_duplicates.exists():
#                 self.add_error('code', "Ya existe un producto con este código.")
#                 raise ValidationError("Ya existe un producto con este código.")

#         return cleaned_data
    


from django import forms
from .models import Products, Category
import unicodedata
from django.utils.text import slugify
import re
from django.core.exceptions import ValidationError

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        labels = {
            'name': 'Name',
            'description': 'Description',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sweet Wine',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter general information, etc.',
                'rows': 3,  
            }),
        }
        error_messages = {
            # Add custom error messages here if needed
        }
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Normalize the name: remove accents, extra spaces, and convert to lowercase
            normalized_name = ''.join(c for c in unicodedata.normalize('NFD', name)
                                    if unicodedata.category(c) != 'Mn')
            normalized_name = re.sub(r'\s+', '', normalized_name.lower())
            
            instance = self.instance
            # Search for existing categories with similar names
            existing_categories = Category.objects.exclude(id=instance.id)
            for category in existing_categories:
                category_normalized = ''.join(c for c in unicodedata.normalize('NFD', category.name)
                                            if unicodedata.category(c) != 'Mn')
                category_normalized = re.sub(r'\s+', '', category_normalized.lower())
                if category_normalized == normalized_name:
                    raise ValidationError(f"A similar category already exists: '{category.name}'")
        return name

        
class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['code', 'category', 'name', 'description', 'price', 'status','cost','quantity']
        labels = {
            'code': 'Code',
            'category': 'Category',
            'name': 'Product Name',
            'description': 'Description',
            'price': 'Price',
            'status': 'Status',
            'cost': 'Cost',
            'quantity': 'Quantity',
        }
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Wine001',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sweet Wine',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter general information, etc.',
                'rows': 3,
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the product price',
                'step': '0.01',
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
            }, choices=[
                (1, 'Active'),
                (0, 'Inactive')
            ]),
             'cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product cost',
                'step': '0.01',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product quantity',
                'min': '0',
            }),
        }
        error_messages = {
            'code': {
                'required': 'This field is required.',
                'max_length': 'This field cannot exceed 100 characters.',
            },
            'category': {
                'required': 'This field is required.',
            },
            'name': {
                'required': 'This field is required.',
            },
            'description': {
                'required': 'This field is required.',
            },
            'price': {
                'required': 'This field is required.',
                'invalid': 'Enter a valid price.',
            },
            'status': {
                'required': 'This field is required.',
                'invalid': 'Enter a valid status.',
            }
        }
    def __init__(self, *args, **kwargs):
        super(ProductsForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            if field.errors:
                field.widget.attrs['class'] += ' is-invalid'
                
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Sort the queryset of category alphabetically
        self.fields['category'].queryset = Category.objects.all().order_by('name')
        # Set the field as non-editable
        self.fields['status'].disabled = True
    
    
    @staticmethod
    def normalize_text(text):
        if text:
            # Remove accents and convert to lowercase
            text = ''.join(c for c in unicodedata.normalize('NFD', text)
                        if unicodedata.category(c) != 'Mn')
            # Remove special characters and spaces
            text = re.sub(r'[^\w]', '', text.lower())
        return text
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        code = cleaned_data.get('code')

        if name and code:
            normalized_name = self.normalize_text(name)
            normalized_code = self.normalize_text(code)

            # Get the current instance if editing
            instance_id = self.instance.pk if self.instance.pk else None

            # Check for duplicate names
            name_duplicates = Products.objects.all()
            if instance_id:
                name_duplicates = name_duplicates.exclude(pk=instance_id)
            
            for product in name_duplicates:
                if self.normalize_text(product.name) == normalized_name:
                    self.add_error('name', "A product with a similar name already exists.")
                    raise ValidationError("A product with a similar name already exists.")

            # Check for duplicate codes
            code_duplicates = Products.objects.filter(code__iexact=normalized_code)
            if instance_id:
                code_duplicates = code_duplicates.exclude(pk=instance_id)
            if code_duplicates.exists():
                self.add_error('code', "A product with this code already exists.")
                raise ValidationError("A product with this code already exists.")

        return cleaned_data