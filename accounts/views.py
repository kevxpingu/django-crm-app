from django.shortcuts import render, redirect
from .models import *
from .forms import orderForm, createUserForm
from .filters import orderFilter
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = createUserForm()
        if request.method == 'POST':
            form = createUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get("username")
                messages.success(request, "Account successfully created for " + user)
                return redirect('login')

        context = {'form': form}
        return render(request, "accounts/register.html", context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "Incorrect Username or Password")
            
        context = {}
        return render(request, "accounts/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect('login')
    

@login_required(login_url="login")
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

@login_required(login_url="login")
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

@login_required(login_url="login")
def products(request):
    products = Product.objects.all()
    return render(request, "accounts/products.html", {'products': products})

@login_required(login_url="login")
def createOrder(request):
    form = orderForm()
    if request.method == 'POST':
        form = orderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, "accounts/order_form.html", context)

@login_required(login_url="login")
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

@login_required(login_url="login")
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    context = {'item':order}
    if request.method == 'POST':
        order.delete()
        return redirect("/")
    return render(request, 'accounts/delete_order.html', context)
        
