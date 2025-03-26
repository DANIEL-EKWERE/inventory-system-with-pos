from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from inventory.models import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from django.contrib import messages
from django.utils import translation
from django.utils.dateformat import DateFormat

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

from django.db import transaction



# from django.utils.translation import gettext as _

# messages.success(request, _('An email has been sent with instructions to reset your password.'))



@login_required
@permission_required('pos.view_sales', raise_exception=True)
def pos(request):
    
    
    products = Products.objects.filter(status=1).order_by('name')
    product_json = []
    for product in products:
        product_json.append({'id': product.id, 'name': product.name, 'price': float(product.price)})
    context = {
        'page_title': "Point of Sale",
        'products': products,
        'product_json': json.dumps(product_json)
    }
    return render(request, 'pos/pos.html', context)


@login_required
@permission_required('pos.view_creditors', raise_exception=True)
def creditors(request):
    creditors = Creditor.objects.order_by('-date_added').all()

    context = {
        'page_title': 'Creditors Transactions',
        'creditor_data': creditors
        }
    
    return render(request, 'pos/creditor.html', context)

import logging
logger = logging.getLogger(__name__)

@login_required
def checkout_modal(request):


            # Extremely verbose logging
    logger.error("=== FULL REQUEST DEBUG START ===")
    logger.error(f"Method:checkout modal {request.method}")
    logger.error(f"POST Data:checkout modal {request.POST}")
    logger.error(f"FILES Data:checkout modal {request.FILES}")
   



    grand_total = 0
    if 'grand_total' in request.GET:
        grand_total = request.GET['grand_total']
    context = {
        'grand_total': grand_total,
    }
    return render(request, 'pos/checkout.html', context)


@login_required
@permission_required('pos.add_sales', raise_exception=True)
@csrf_exempt
def save_pos(request):
    resp = {'status': 'failed', 'msg': ''}
    data = request.POST

    # Generate a unique sale code
    pref = datetime.now().year + datetime.now().year
    i = 1
    while True:
        code = '{:0>5}'.format(i)
        i += 1
        check = Sales.objects.filter(code=str(pref) + str(code)).exists()
        if not check:
            break
    code = str(pref) + str(code)

    try:
        with transaction.atomic():  # Start a database transaction
            # Create the Sales record
            sales = Sales(
                code=code,
                sub_total=data['sub_total'],
                tax=data['tax'],
                tax_amount=data['tax_amount'],
                grand_total=data['grand_total'],
                tendered_amount=data['tendered_amount'],
                amount_change=data['amount_change']
            )
            sales.save()

            # Process each product in the sale
            sale_id = sales.pk
            i = 0
            for prod_id in data.getlist('product[]'):
                product = get_object_or_404(Products, id=prod_id)
                qty = int(data.getlist('qty[]')[i])
                
                price = float(data.getlist('price[]')[i])
                total = qty * price

                # Check if the product has sufficient stock
                if product.quantity < qty:
                    raise ValueError(f"Not enough stock for product '{product.name}'.")

                # Deduct the quantity from the product
                # product.quantity -= qty
                # product.save(update_fields=['quantity'])

                # Create the salesItems record
                sales_item = salesItems(
                    sale=sales,
                    product=product,
                    qty=qty,
                    price=price,
                    total=total
                )
                sales_item.save()
                i += 1


                # Payment type and amount checks
            tendered_amount = float(request.POST.get('tendered_amount', 0))
            grand_total = float(request.POST.get('grand_total', 0))
            payment_type = request.POST.get('payment_type', 'full')

            customer_name = request.POST.get('customer_name', '').strip()
            customer_phone = request.POST.get('customer_phone', '').strip()
            customer_address = request.POST.get('customer_address', '').strip()
            customer_email = request.POST.get('customer_email', 'N/A').strip()
            
            # Detailed logging
            print("Partial Payment Details:")
            print(f"Customer Name: {customer_name}")
            print(f"Customer Phone: {customer_phone}")
            print(f"Customer Address: {customer_address}")
            print(f"Customer Email: {customer_email}")
            
            # Partial payment specific logic
            if payment_type == 'partial' and tendered_amount < grand_total:
                # Extract customer details
                customer_name = request.POST.get('customer_name', '').strip()
                customer_phone = request.POST.get('customer_phone', '').strip()
                customer_address = request.POST.get('customer_address', '').strip()
                customer_email = request.POST.get('customer_email', 'N/A').strip()
                
                # Detailed logging
                print("Partial Payment Details:")
                print(f"Customer Name: {customer_name}")
                print(f"Customer Phone: {customer_phone}")
                print(f"Customer Address: {customer_address}")
                print(f"Customer Email: {customer_email}")
                
                # Validate required fields
                if not (customer_name and customer_phone and customer_address):
                    resp['msg'] = "Customer name, phone, and address are required for partial payments."
                    return JsonResponse(resp)
                
                # Create Creditor record
                creditor = Creditor.objects.create(
                    sale_id=code,
                    customer=customer_name,
                    phone=customer_phone,
                    email=customer_email,
                    address=customer_address,
                    amount=grand_total,
                    balance=grand_total - tendered_amount,
                    paid_amount=tendered_amount,
                )
                
                print(f"Creditor record created: {creditor.id}")
                messages.success(request, "Partial payment recorded. Creditor record created.")
            
            resp['status'] = 'success'
            resp['sale'] = sale_id
            messages.success(request, "The sale has been recorded.")
    
    except ValueError as e:
        resp['msg'] = str(e)
    except Exception as e:
        resp['msg'] = "An error occurred: " + str(e)
    
    return JsonResponse(resp)

@login_required
@permission_required('pos.view_sales', raise_exception=True)
def salesList(request):
    sales = Sales.objects.order_by('-date_added').all()
    sale_data = []
    for sale in sales:
        data = {}
        for field in sale._meta.get_fields(include_parents=False):
            if field.related_model is None:
                data[field.name] = getattr(sale, field.name)
        items = salesItems.objects.filter(sale_id=sale).all()
        products_list = {}
        for item in items:
            product_name = item.product.name
            if product_name in products_list:
                products_list[product_name] += item.qty
            else:
                products_list[product_name] = item.qty
        data['products_list'] = products_list
        data['total_items_sold'] = sum(products_list.values())
        if 'tax_amount' in data:
            data['tax_amount'] = format(float(data['tax_amount']), '.2f')
        sale_data.append(data)
    context = {
        'page_title': 'Sales Transactions',
        'sale_data': sale_data,
    }
    return render(request, 'pos/sales.html', context)

@login_required
# @permission_required('pos.view_creditor', raise_exception=True)
def credior(request):
    creditors = Creditor.objects.order_by('-date_added').all()
    # creditor_data = []
    # for creditor in creditors:
    #     data = {}
    #     for field in creditor._meta.get_fields(include_parents=False):
    #         if field.related_model is None:
    #             data[field.name] = getattr(creditor, field.name)
    #     creditor_data.append(data)
    context = {
        'page_title': 'Creditors Transactions',
        'creditor_data': creditors,
    }
    return render(request, 'pos/creditor.html', context)


@login_required
@permission_required('pos.add_sales', raise_exception=True)
def create_sales_item(request, product_id, qty, sale_instance):
    product = get_object_or_404(Products, id=product_id)
    print(f'quantity {qty}')
    try:
        qty = int(qty)
        if product.quantity < qty:
            return JsonResponse({"error": "There is not enough product quantity to sell."}, status=400)
        sales_item = salesItems.objects.create(
            product=product,
            qty=qty,
            price=product.price,
            total=product.price * qty,
            sale=sale_instance
        )
        product.update_quantity_on_sale(qty)
        return JsonResponse({"success": "Sales item created successfully."})
    except ValueError:
        return JsonResponse({"error": "Invalid quantity."}, status=400)

@login_required
@permission_required('pos.add_sales', raise_exception=True)
@csrf_exempt
def create_sale(request):
    if request.method == "POST":
        sale_code = request.POST.get('code')
        items = json.loads(request.POST.get('items'))

        sale = Sales.objects.create(
            code=sale_code,
            sub_total=0,
            grand_total=0,
            tax_amount=0,
            tax=0,
            tendered_amount=0,
            amount_change=0,
        )

        for item in items:
            product_id = item['product_id']
            qty = item['qty']
            response = create_sales_item(request, product_id, qty, sale)
            if response.status_code == 400:
                sale.delete()
                return response

        sale.sub_total = sum([item.total for item in sale.salesitems_set.all()])
        sale.tax_amount = sale.sub_total * (sale.tax / 100)
        sale.grand_total = sale.sub_total + sale.tax_amount
        sale.save()

        return JsonResponse({"success": "Sales Created Successfully."})

    return JsonResponse({"error": "No Permission."}, status=405)

@login_required
def receipt(request):
    id = request.GET.get('id')
    sales = Sales.objects.filter(id=id).first()
    transaction = {}
    for field in Sales._meta.get_fields():
        if field.related_model is None: 
            transaction[field.name] = getattr(sales, field.name)
    if 'tax_amount' in transaction:
        transaction['tax_amount'] = format(float(transaction['tax_amount']))
    ItemList = salesItems.objects.filter(sale=sales).all()
    
        # Cambiar el idioma a español para la fecha
    with translation.override('en-us'):
        formatted_date = DateFormat(sales.date_added).format('d F Y')
    context = {
        "transaction": transaction,
        "salesItems": ItemList,
        
        "formatted_date": formatted_date,
    }
    return render(request, 'pos/receipt.html', context)

@login_required
@permission_required('pos.delete_sales', raise_exception=True)
def delete_sale(request):
    resp = {'status': 'failed', 'msg': ''}
    id = request.POST.get('id')
    try:
        sale = Sales.objects.get(id=id)
        with transaction.atomic():
            for item in sale.salesitems_set.all():
                item.delete()
            sale.delete()
        resp['status'] = 'success'
        messages.success(request, 'The sale record was deleted, and the product quantities were restored.')
    except Sales.DoesNotExist:
        resp['msg'] = "La venta no existe"
    except Exception as e:
        resp['msg'] = f"Ocurrió un error: {str(e)}"
    return HttpResponse(json.dumps(resp), content_type='application/json')

def error_403(request, exception=None):
    return render(request, 'errors/403.html', status=403)
