import json
from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .models import Sale, SaleItem
from django.contrib.auth.decorators import login_required
from inventory.models import Drug
from accounts.decorators import role_required
from accounts.models import Customer

# Create your views here.
@login_required
@role_required('ADMIN', 'MANAGER', 'WHOLESALER')
def wholesale(request):
    drugs = Drug.objects.filter(inventory__gt=0)
    customers = Customer.objects.all().order_by('name')
    return render(request, 'sales/wholesaleUI.html', {
        'drugs':drugs,
        'customers': customers
    })

@login_required
@role_required('ADMIN', 'MANAGER', 'WHOLESALER')
def process_wholesale_sale(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        items = data.get('items', [])
        customer_id = data.get('customer_id')

        if not items:
            return JsonResponse({'success': False, 'message': 'No items in cart'}, status=400)

        with transaction.atomic():
            customer = None
            if customer_id:
                customer = get_object_or_404(Customer, id=customer_id)

            sale = Sale.objects.create(
                seller=request.user,
                type=Sale.SaleType.WHOLESALE,
                customer=customer
            )

            for item in items:
                drug = get_object_or_404(Drug, id=item['id'])
                quantity = int(item['quantity'])
                
                SaleItem.objects.create(
                    sale=sale,
                    drug=drug,
                    quantity=quantity,
                )

        return JsonResponse({
            'success': True,
            'message': 'Sale processed successfully',
            'sale_id': sale.id,
            'updated_stock': [
                {'id': item.drug.id, 'inventory':item.drug.inventory}
                for item in sale.saleitem_set.all()
            ]
        })

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        return JsonResponse({'success': False, 'message': f'Invalid data: {str(e)}'}, status=400)
    except ValidationError as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Server error: {str(e)}'}, status=500)
    
@login_required
@role_required('ADMIN', 'MANAGER', 'RETAILER')
def retail(request):
    drugs = Drug.objects.filter(inventory__gt=0)
    customers = Customer.objects.all().order_by('name')
    return render(request, 'sales/retailUI.html', {
        'drugs':drugs,
        'customers': customers
    })

@login_required
@role_required('ADMIN', 'MANAGER', 'RETAILER')
def process_retail_sale(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        items = data.get('items', [])
        customer_id = data.get('customer_id')

        if not items:
            return JsonResponse({'success': False, 'message': 'No items in cart'}, status=400)

        with transaction.atomic():
            customer = None
            if customer_id:
                customer = get_object_or_404(Customer, id=customer_id)

            sale = Sale.objects.create(
                seller=request.user,
                type=Sale.SaleType.RETAIL,
                customer=customer
            )

            for item in items:
                drug = get_object_or_404(Drug, id=item['id'])
                quantity = int(item['quantity'])
                
                SaleItem.objects.create(
                    sale=sale,
                    drug=drug,
                    quantity=quantity,
                )

        return JsonResponse({
            'success': True,
            'message': 'Sale processed successfully',
            'sale_id': sale.id,
            'updated_stock': [
                {'id': item.drug.id, 'inventory':item.drug.inventory}
                for item in sale.saleitem_set.all()
            ]
        })

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        return JsonResponse({'success': False, 'message': f'Invalid data: {str(e)}'}, status=400)
    except ValidationError as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Server error: {str(e)}'}, status=500)
    

    
@login_required
@role_required('ADMIN', 'MANAGER')
def sales_list(request):
    sales = Sale.objects.all().order_by('-created_at')
    return render(request, 'sales/sales_list.html', {
        'sales': sales
    })

@login_required
def generate_receipt(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    return render(request, 'sales/receipt.html', {'sale': sale})
