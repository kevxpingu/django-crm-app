from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import orderForm
from .filters import orderFilter

# Create your views here.

def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_orders = orders.count()
    orders_pending = orders.filter(status="Pending").count()
    orders_delivered = orders.filter(status="Delivered").count()
    context = {
        'customers': customers,
        'orders': orders,
        'total_orders': total_orders,
        'orders_pending': orders_pending,
        'orders_delivered': orders_delivered
    }
    return render(request, 'accounts/dashboard.html', context)

def customers(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    total_order = orders.count()

    myFilter = orderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {
        'customer': customer,
        'orders': orders,
        'total_order': total_order,
        'myFilter': myFilter
    }
    return render(request, "accounts/customers.html", context)

def products(request):
    products = Product.objects.all()
    return render(request, "accounts/products.html", {'products': products})

def createOrder(request):
    form = orderForm()
    if request.method == 'POST':
        form = orderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, "accounts/order_form.html", context)

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = orderForm(instance=order)
    if request.method == 'POST':
        form = orderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, "accounts/order_form.html", context)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    context = {'item':order}
    if request.method == 'POST':
        order.delete()
        return redirect("/")
    return render(request, 'accounts/delete_order.html', context)
        
