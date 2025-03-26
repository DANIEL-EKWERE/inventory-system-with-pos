# from django import forms
# from pos.models import Sales
# from datetime import datetime
# from django import forms

# from purchase.models import *
# MONTH_NAMES = [
#     'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
#     'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
# ]


# MONTH_CHOICES = [(str(i), month) for i, month in enumerate(MONTH_NAMES, 1)]


# DAYS_OF_WEEK = {
#     'Monday': 'Lunes',
#     'Tuesday': 'Martes',
#     'Wednesday': 'Miércoles',
#     'Thursday': 'Jueves',
#     'Friday': 'Viernes',
#     'Saturday': 'Sábado',
#     'Sunday': 'Domingo'
# }

# class SalesReportForm(forms.Form):
#     start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
#     end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
#     customer = forms.CharField(max_length=100, required=False)


# class YearMonthForm(forms.Form):
#     year = forms.IntegerField(label="Año", min_value=1900, max_value=2100)
#     month = forms.ChoiceField(label="Mes", choices=MONTH_CHOICES)


# class YearForm(forms.Form):
#     year = forms.IntegerField(label="Año", min_value=1900, max_value=2100)


# class DayForm(forms.Form):
#     year = forms.IntegerField(label="Año", min_value=1900, max_value=2100)
#     month = forms.ChoiceField(label="Mes", choices=MONTH_CHOICES)
#     day = forms.IntegerField(label="Día", min_value=1, max_value=31)


# class DateRangeForm(forms.Form):
#     fecha_desde = forms.DateField(label="Fecha desde", widget=forms.DateInput(attrs={'type': 'date'}))
#     fecha_hasta = forms.DateField(label="Fecha hasta", widget=forms.DateInput(attrs={'type': 'date'}))


# class ReportForm(forms.Form):
#     pass

# class MonthReportForm(forms.Form):
#     year = forms.IntegerField(label='Año', min_value=1900, max_value=datetime.now().year)
#     month = forms.IntegerField(label='Mes', min_value=1, max_value=12)

# class DayReportForm(forms.Form):
#     year = forms.IntegerField(label='Año', min_value=1900, max_value=datetime.now().year)
#     month = forms.IntegerField(label='Mes', min_value=1, max_value=12)
#     day = forms.IntegerField(label='Día', min_value=1, max_value=31)

# class PurchaseReportForm(forms.Form):
#     start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
#     end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
#     supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=False)


# class YearReportForm(forms.Form):
#     current_year = datetime.now().year
#     YEAR_CHOICES = [(year, year) for year in range(current_year - 10, current_year + 1)]

#     year = forms.ChoiceField(choices=YEAR_CHOICES, required=True, label="Seleccione el Año", widget=forms.Select)

# class MonthYearReportForm(forms.Form):
#     year = forms.IntegerField(min_value=2000, max_value=timezone.now().year, label='Año')
#     month = forms.IntegerField(min_value=1, max_value=12, label='Mes')

# class DayMonthYearReportForm(forms.Form):
#     year = forms.IntegerField(min_value=2000, max_value=timezone.now().year, label='Año')
#     month = forms.IntegerField(min_value=1, max_value=12, label='Mes')
#     day = forms.IntegerField(min_value=1, max_value=31, label='Día')  # Nota: No valida días específicos para cada mes

# class DayTramoForm(forms.Form):
#     start_year = forms.IntegerField(label='Año Inicio', min_value=2023)
#     start_month = forms.ChoiceField(label='Mes Inicio', choices=[
#         ('', 'Mes'),
#         (1, 'Enero'),
#         (2, 'Febrero'),
#         (3, 'Marzo'),
#         (4, 'Abril'),
#         (5, 'Mayo'),
#         (6, 'Junio'),
#         (7, 'Julio'),
#         (8, 'Agosto'),
#         (9, 'Septiembre'),
#         (10, 'Octubre'),
#         (11, 'Noviembre'),
#         (12, 'Diciembre'),
#     ])
#     start_day = forms.IntegerField(label='Día Inicio', min_value=1, max_value=31)

#     end_year = forms.IntegerField(label='Año Fin', min_value=2023)
#     end_month = forms.ChoiceField(label='Mes Fin', choices=[
#         ('', 'Mes'),
#         (1, 'Enero'),
#         (2, 'Febrero'),
#         (3, 'Marzo'),
#         (4, 'Abril'),
#         (5, 'Mayo'),
#         (6, 'Junio'),
#         (7, 'Julio'),
#         (8, 'Agosto'),
#         (9, 'Septiembre'),
#         (10, 'Octubre'),
#         (11, 'Noviembre'),
#         (12, 'Diciembre'),
#     ])
#     end_day = forms.IntegerField(label='Día Fin', min_value=1, max_value=31)




from django import forms
from pos.models import Sales
from datetime import datetime
from django import forms

from purchase.models import *
MONTH_NAMES = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]  # Translated from Spanish month names

MONTH_CHOICES = [(str(i), month) for i, month in enumerate(MONTH_NAMES, 1)]

DAYS_OF_WEEK = {
    'Monday': 'Monday',
    'Tuesday': 'Tuesday',
    'Wednesday': 'Wednesday',
    'Thursday': 'Thursday',
    'Friday': 'Friday',
    'Saturday': 'Saturday',
    'Sunday': 'Sunday'
}  # No translation needed for days of the week

class SalesReportForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    customer = forms.CharField(max_length=100, required=False)


class YearMonthForm(forms.Form):
    year = forms.IntegerField(label="Year", min_value=1900, max_value=2100)  # Translated from "Año"
    month = forms.ChoiceField(label="Month", choices=MONTH_CHOICES)  # Translated from "Mes"


class YearForm(forms.Form):
    year = forms.IntegerField(label="Year", min_value=1900, max_value=2100)  # Translated from "Año"


class DayForm(forms.Form):
    year = forms.IntegerField(label="Year", min_value=1900, max_value=2100)  # Translated from "Año"
    month = forms.ChoiceField(label="Month", choices=MONTH_CHOICES)  # Translated from "Mes"
    day = forms.IntegerField(label="Day", min_value=1, max_value=31)  # Translated from "Día"


class DateRangeForm(forms.Form):
    start_date = forms.DateField(label="Start Date", widget=forms.DateInput(attrs={'type': 'date'}))  # Translated from "Fecha desde"
    end_date = forms.DateField(label="End Date", widget=forms.DateInput(attrs={'type': 'date'}))  # Translated from "Fecha hasta"


class ReportForm(forms.Form):
    pass

class MonthReportForm(forms.Form):
    year = forms.IntegerField(label='Year', min_value=1900, max_value=datetime.now().year)  # Translated from "Año"
    month = forms.IntegerField(label='Month', min_value=1, max_value=12)  # Translated from "Mes"

class DayReportForm(forms.Form):
    year = forms.IntegerField(label='Year', min_value=1900, max_value=datetime.now().year)  # Translated from "Año"
    month = forms.IntegerField(label='Month', min_value=1, max_value=12)  # Translated from "Mes"
    day = forms.IntegerField(label='Day', min_value=1, max_value=31)  # Translated from "Día"

class PurchaseReportForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=False)


class YearReportForm(forms.Form):
    current_year = datetime.now().year
    YEAR_CHOICES = [(year, year) for year in range(current_year - 10, current_year + 1)]

    year = forms.ChoiceField(choices=YEAR_CHOICES, required=True, label="Select the Year", widget=forms.Select)  # Translated from "Seleccione el Año"

class MonthYearReportForm(forms.Form):
    year = forms.IntegerField(min_value=2000, max_value=timezone.now().year, label='Year')  # Translated from "Año"
    month = forms.IntegerField(min_value=1, max_value=12, label='Month')  # Translated from "Mes"

class DayMonthYearReportForm(forms.Form):
    year = forms.IntegerField(min_value=2000, max_value=timezone.now().year, label='Year')  # Translated from "Año"
    month = forms.IntegerField(min_value=1, max_value=12, label='Month')  # Translated from "Mes"
    day = forms.IntegerField(min_value=1, max_value=31, label='Day')  # Translated from "Día"

class DayTramoForm(forms.Form):
    start_year = forms.IntegerField(label='Start Year', min_value=2023)  # Translated from "Año Inicio"
    start_month = forms.ChoiceField(label='Start Month', choices=[
        ('', 'Month'),  # Translated from "Mes"
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    ])
    start_day = forms.IntegerField(label='Start Day', min_value=1, max_value=31)  # Translated from "Día Inicio"

    end_year = forms.IntegerField(label='End Year', min_value=2023)  # Translated from "Año Fin"
    end_month = forms.ChoiceField(label='End Month', choices=[
        ('', 'Month'),  # Translated from "Mes"
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    ])
    end_day = forms.IntegerField(label='End Day', min_value=1, max_value=31)  # Translated from "Día Fin"