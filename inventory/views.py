from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.contrib import messages
from django.http import HttpResponse
from .models import Drug
from .forms import DrugForm
from sales.models import Sale, SaleItem
from datetime import timedelta
from accounts.models import User
from accounts.decorators import role_required
import csv


# Create your views here.

@login_required
def home(request):
    now = timezone.now()

    monthly_sale = Sale.objects.filter(created_at__month=now.month, created_at__year=now.year).aggregate(total=Sum('total_cost'))

    last_month = now - timedelta(days=30)

    last_month_sales = Sale.objects.filter(
        created_at__month=last_month.month,
        created_at__year=last_month.year
    ).aggregate(total=Sum('total_cost'))

    this_month_total = monthly_sale['total'] or 0
    last_month_total = last_month_sales['total'] or 0

    try:
        revenue_percentage_change = ((this_month_total - last_month_total) / last_month_total) * 100
    except ZeroDivisionError:
        revenue_percentage_change = 0

    this_month_sales_count = Sale.objects.filter(
        created_at__month=now.month, 
        created_at__year=now.year
    ).count()

    last_month_sales_count = Sale.objects.filter(
        created_at__month=last_month.month,
        created_at__year=last_month.year
    ).count()

    try:
        sales_count_change = ((this_month_sales_count - last_month_sales_count) / last_month_sales_count) * 100
    except ZeroDivisionError:
        sales_count_change = 0

    total_drugs = Drug.objects.count()

    users_count = User.objects.filter(is_superuser=False).count()

    six_months_ago = now - timedelta(days=180)
    monthly_data = SaleItem.objects.filter(sale__created_at__gte=six_months_ago).annotate(
        month=TruncMonth('sale__created_at')
    ).values('month').annotate(
        revenue=Sum('total_cost'),
        profit=Sum(
            ExpressionWrapper(
                F('total_cost') - F('drug__cost_price') * F('quantity'),
                output_field=DecimalField()
            )
        ),
        sales_count=Count('sale')
    ).order_by('month')

    chart_data = [
        {
            'month': item['month'].strftime('%b'),
            'revenue': float(item['revenue']),
            'profit': float(item['profit']),
            'sales_count': item['sales_count']
        }
        for item in monthly_data
    ]

    context = {
        'this_month_total': this_month_total,
        'last_month_total': last_month_total,
        'revenue_percentage_change': round(revenue_percentage_change, 1),
        'sales_count_change': round(sales_count_change, 1),
        'this_month_sales_count':this_month_sales_count,
        'total_drugs': total_drugs,
        'users_count': users_count,
        'chart_data': chart_data,
        'recent_sales': Sale.objects.all().order_by('-created_at')[:5]
    }

    return render(request, 'inventory/dashboard.html', context)



@role_required('ADMIN', 'MANAGER')
def drug_list(request):
    drugs = Drug.objects.all().order_by('id')
    return render(request, 'inventory/drug_list.html', {
        'drugs': drugs
    })


@role_required('ADMIN', 'MANAGER')
def update_drug(request, drug_id):
    if request.method == 'POST':
        drug = get_object_or_404(Drug, id=drug_id)

        name = request.POST.get('name', drug.name)
        wholesale_price = request.POST.get('wholesale_price', drug.wholesale_price)
        retail_price = request.POST.get('retail_price', drug.retail_price)
        inventory = request.POST.get('inventory', drug.inventory)

        drug.name = name
        drug.wholesale_price = wholesale_price
        drug.retail_price = retail_price
        drug.inventory = inventory
        
        try:
            drug.save()
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
        
        return JsonResponse({
            'success': True,
            'message': 'Drug updated successfully',
            'drug': {
                'name': drug.name,
                'wholesale_price': str(drug.wholesale_price),
                'retail_price': str(drug.retail_price),
                'inventory': drug.inventory
            }
        })
    
    return JsonResponse({
        'success':False,
        'message': 'Invalid request'
    }, status=400)

@require_POST
@role_required('ADMIN', 'MANAGER')
def delete_drug(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)
    try:
        drug.delete()
        return JsonResponse({'success': True, 'message': 'Drug deleted successfully'})
    except ProtectedError:
        return JsonResponse({'success': False, 'message': 'Cannot delete drug with existing sales records'}, status=400)

@login_required
@role_required('ADMIN', 'MANAGER')
def create_drug(request):
    if request.method == 'POST':
        form = DrugForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Drug added successfully!')
            return redirect('inventory:drug_list')
    else:
        form = DrugForm()
    
    return render(request, 'inventory/create_drug.html', {
        'form': form,
        'title': 'Add New Drug'
    })


def export_inventory_csv(request):
    response = HttpResponse(content_type='text/csv')

    filename = f"inventory_{timezone.now().strftime('%Y-%m-%d')}.csv"

    response['Content-Disposition'] = f'attachment; filename={filename}'

    writer = csv.writer(response)

    writer.writerow(['Drug Name', 'Wholesale Price', 'Retail Price', 'Stock Level', 'Expiry Date'])

    drugs = Drug.objects.all().order_by('name')
    for drug in drugs:
        writer.writerow([
            drug.name,
            drug.wholesale_price,
            drug.retail_price,
            drug.inventory,
            drug.expiry_date  
        ])
    
    return response