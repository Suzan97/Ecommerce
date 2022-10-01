from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import *
# from django.contrib.auth.hashers import make_password

# class CustomerForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password','gender']

#     def save(self, commit=True):
#         user = super(CustomerForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']
#         if commit:
#             user.save()
#         return user

class CustomerSignUpForm(UserCreationForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    gender = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def data_save(self):
        user = super().save(commit=False)
        user.name = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(user=user)
        customer.gender = self.cleaned_data.get('gender')
        customer.phone_number = self.cleaned_data.get('phone_number')
        customer.save()
        return user


class VendorSignUpForm(UserCreationForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    service = forms.ModelChoiceField(queryset=Service.objects.all())
    comp_name = forms.CharField(required=True)
    comp_reg_no = forms.CharField(required=True)
    location = forms.CharField(required=True)
    city = forms.ModelChoiceField(queryset=City.objects.all())

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def data_save(self):
        user = super().save(commit=False)
        user.name = self.cleaned_data.get('name')
        user.email = self.cleaned_data.get('email')
        user.is_vendor = True
        user.save()
        vendor = vendor.objects.create(user=user)
        vendor.phone_number = self.cleaned_data.get('phone_number')
        vendor.service = self.cleaned_data.get('service')
        vendor.comp_name= self.cleaned_data.get('company name')
        vendor.comp_reg_no = self.cleaned_data.get('Company Registration Number')
        vendor.location = self.cleaned_data.get('location')
        vendor.city = self.cleaned_data.get('city')
        vendor.save()
        return user