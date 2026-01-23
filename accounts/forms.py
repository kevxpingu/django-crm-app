from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order
from .models import Customer
from django import forms

class orderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class createUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class customerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']