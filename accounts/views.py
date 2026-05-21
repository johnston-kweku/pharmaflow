from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .decorators import role_required
from .forms import UserCreationForm, CustomerForm
from .models import Customer

User = get_user_model()
# Create your views here.

@login_required
def customer_list(request):
    customers = Customer.objects.all().order_by('name')
    return render(request, 'accounts/customer_list.html', {'customers': customers})

@login_required
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer created successfully!')
            return redirect('accounts:customer_list')
    else:
        form = CustomerForm()
    return render(request, 'accounts/create_customer.html', {'form': form})

@login_required
def update_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully!')
            return redirect('accounts:customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'accounts/create_customer.html', {
        'form': form,
        'title': 'Update Customer'
    })

@login_required
@role_required('ADMIN', 'MANAGER')
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    messages.success(request, 'Customer deleted successfully!')
    return redirect('accounts:customer_list')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('inventory:home')

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        role = request.POST.get('role', '')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.role == role:
                if not user.is_active:
                    messages.error(request, "Your account is inactive. Please contact an admin.")
                else:
                    auth_login(request, user)
                    if user.is_admin() or user.is_manager():
                        return redirect('inventory:home')
                    elif user.is_wholesaler():
                        return redirect('sales:wholesale')
                    elif user.is_retailer():
                        return redirect('sales:retail')
            else:
                messages.error(request, f"Invalid role selected for this user.")
        else:
            messages.error(request, "Invalid username or password.")
        
    return render(request, 'accounts/login.html')




def logout_view(request):
    logout(request)
    return redirect('accounts:login')



@role_required('ADMIN', 'MANAGER')
def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            if request.user.can_create_role(role):
                form.save()
                return redirect('accounts:user_list')
            else:
                form.add_error('role', 'You do not have permission to create this role')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/create_user.html', {'form': form})


@role_required('ADMIN', 'MANAGER')
def user_list(request):
    users = User.objects.filter(is_superuser=False)
    return render(request, 'accounts/user_list.html', {'users': users})


@role_required('ADMIN', 'MANAGER')
def toggle_user_active(request, username):
    user = get_object_or_404(User, username=username)
    if user.is_superuser: 
        return JsonResponse({
            'success': False,
            'is_active': True,
            'message': 'Cannot deactivate this user'
        })
    
    if user.is_active:
        user.is_active = False
        user.save()
        return JsonResponse({
            'success': True,
            'is_active': False,
            'message': 'User deactivated successfully'
        })
    else:
        user.is_active = True
        user.save()
        return JsonResponse({
            'success': True,
            'is_active': True,
            'message': 'User activated successfully'
        })

    