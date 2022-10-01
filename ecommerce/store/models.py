from enum import unique
from itertools import product
from random import choices
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from hashid_field import HashidAutoField
from django_extensions.db.fields import AutoSlugField
from django.forms import ModelForm
# Create your models here.

TITLE_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('PNS', 'Prefer not to say'),
]
class Service(models.Model):
    name = models.CharField(max_length= 50, null = False)

    def __str__(self):
        return self.name

class City(models.Model):
    city = models.CharField(max_length= 100, null = False)

    def __str__(self):
        return self.city

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=80)


class Customer(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=10)
    gender = models.CharField(max_length=7, choices=TITLE_CHOICES, null = True)

class Vendor(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=10)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    comp_name = models.CharField(max_length=200, null=False)
    comp_reg_no = models.CharField(max_length=200, null=False)
    location = models.CharField(max_length = 200, null = False)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)



# class Customer(models.Model):
#     user  = models.OneToOneField(User,null = True, blank=True, on_delete=models.CASCADE)
#     username = models.CharField(max_length=200)
#     password = models.CharField(max_length=100, null = True)
#     email = models.EmailField(max_length=200, null = True, unique = True)
#     gender = models.CharField(max_length=3, choices=TITLE_CHOICES, null = True)

#     def __str__(self):
#         return self.username


class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank = 
    True, null=True)
    title = models.CharField(max_length=100) 
    slug = AutoSlugField(populate_from='title', unique=True, null=False, editable=False)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        #enforcing that there can not be two categories under a parent with same slug

        # __str__ method elaborated later in post.  use __unicode__ in place of

        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories"     

    def __str__(self):                           
        full_path = [self.title]                  
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1]) 


class Product(models.Model):
    id = HashidAutoField(primary_key=True, min_length=9)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null = True)
    image = models.ImageField(null = True, blank=True)
    image2 = models.ImageField(null = True, blank=True)
    image3 = models.ImageField(null = True, blank=True)
    gen_desc = models.CharField(max_length=500, null=True)
    det_desc  = models.CharField(max_length = 2500, null=True)
    add_desc = models.CharField(max_length=2500, null=True)
    

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    @property
    def imageURL1(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url

    @property
    def imageURL2(self):
        try:
            url = self.image3.url
        except:
            url = ''
        return url



  


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default = 0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total




# class VendorProduct(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
#     fname = models.CharField(max_length=200, null=False)
#     lname = models.CharField(max_length=200, null=False)
#     password = models.CharField(max_length=100, null=False)
#     comp_name = models.CharField(max_length=200, null=False)
#     comp_reg_no = models.CharField(max_length=200, null=False)
#     service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
#     location = models.CharField(max_length = 200, null = False)
#     city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)

#     def __str__(self):
#         return self.fname

    


# class ShippingAddress(models.Model):
#     customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     order = models.ForeignKey(Order, on_delete = models.SET_NULL, null=True)
#     address = models.CharField(max_length=200, null=False)
#     city = models.CharField(max_length=200, null=False)
#     contact = PhoneNumberField(unique = True, null = False, blank = False)
#     zipcode = models.CharField(max_length=200, null=False)
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.address



# class Vendors(models.Model):
