from django.shortcuts import render
from django.http import HttpResponse
from .models import *

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

def customers(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_order = orders.count()
    context = {
        'customer': customer,
        'orders': orders,
        'total_order': total_order
    }
    return render(request, "accounts/customers.html", context)

def products(request):
    products = Product.objects.all()
    return render(request, "accounts/products.html", {'products': products})
