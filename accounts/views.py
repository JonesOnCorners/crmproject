from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .models import *
from accounts.forms import OrderForm, CustomerForm, CreateUserForm
from accounts.filters import OrderFilter 
from accounts.decorators import unauthenticated_users, allowed_users


# Create your views here.


@unauthenticated_users
def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get("username")
        password=request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('index'))
        else:
            messages.error(request,'Kindly Register First.')
            return redirect(reverse('login'))
    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@unauthenticated_users
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()            
            username = form.cleaned_data.get("username")
            
            # group = Group.objects.get(name="customers")

            # user.groups.add(group)

            # Customer.objects.create(user=user)

            
            messages.success(request,'Account successfully Created for user:' + username + '. Kindly Login')
            return redirect(reverse('login'))
    
    context = {'form':form}
    return render(request, 'accounts/register.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()    
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders,
               'pending' : pending,
               'delivered': delivered,
               'total_orders': total_orders
               }
    return render(request, 'accounts/user.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method=='POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
        
    context ={'form':form}
    return render(request,'accounts/accountsettings.html',context)

@allowed_users(allowed_roles=['admin'])
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_orders = orders.count()
    total_customers = customers.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 
               'customers': customers,
               'pending' : pending,
               'delivered': delivered,
               'total_orders': total_orders}
    return render(request,'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    return render(request,'accounts/products.html',{'products' : products})


def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    
    context = {
              'customer': customer,
              'orders' : orders,
              'order_count': order_count,
              'myFilter' : myFilter

    }    
    return render(request,'accounts/customer.html',context)


def createOrder(request, pk):
    orderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra= 5)
    customer = Customer.objects.get(id=pk)
    formset = orderFormSet(queryset=Order.objects.none(),instance=customer)
    #form = OrderForm()
    #print(form)
    if request.method == "POST":
        formset = orderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('index'))
    context ={'formset':formset}
    return render(request,'accounts/orderform.html', context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    context ={'form':form}

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))            
    return render(request,'accounts/orderform.html', context)

def deleteOrder(request, pk):
    item = Order.objects.get(id=pk)
    form = OrderForm(instance=item)
    context ={'item':item}

    if request.method == 'POST':
        item.delete()
        return redirect(reverse('index'))
    
    return render(request,'accounts/deleteorder.html', context)

def createCustomer(request):
    form = CustomerForm()
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    context ={'form':form}
    return render(request,'accounts/customerform.html', context)