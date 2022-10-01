from django.contrib import messages
from email import message
from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse, HttpResponse
import json
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from . forms import *
from django.contrib.auth.hashers import make_password


from . utils import cookieCart, cartData
# Create your views here.

# def signup(request):
#     if request.method == 'POST':
#         form  = CustomerForm(request.POST or None)
#         if form.is_valid():
#             sign_up = form.save(commit=False)
#             sign_up.password = make_password(form.cleaned_data['password'])
#             sign_up.status = 1
#             sign_up.save()
            
#             messages.success(request, f'Your account has been created. You can now login')
#             return redirect('login')
#     else:
#         form = CustomerForm()
   
#     context = {'form': form}
#     return render(request, 'account/signup.html', context)


class customer_register(CreateView):
    model = User  
    form_class = CustomerSignUpForm
    template_name= 'account/cust_signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

class vendor_register(CreateView):
    model = User  
    form_class = VendorSignUpForm
    template_name= 'account/comp_signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

def login_user(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('index')
            else:
                messages.error(request,"Invalid username or password")
        else:
            messages.error(request,"Invalid username or password")
    return render(request, 'login.html',context={'form':AuthenticationForm()})

# def signin(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.info(request, f"You are now logged in as {username}.")
#                 return redirect("homepage")
#             else:
#                 messages.error(request,"Invalid username or password.")
#         else:
#             messages.error(request,"Invalid username or password.")
#     form = AuthenticationForm()
#     return render(request=request, template_name="account/login.html", context={"login_form":form})

# def comp_signup(request):
#     context = {}
#     return render(request, 'account/comp_signup.html', context)

def home(request):
    context = {}
    return render(request, 'account/home.html', context)

def store(request):

    data = cartData(request)
    cartItems =data['cartItems']
    

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/index.html', context)

def shop(request):
    data = cartData(request)
    cartItems =data['cartItems']
    

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/shop.html', context)



def cart(request):

    data = cartData(request)
    cartItems =data['cartItems']
    order = data['order']
    items = data['items']


    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def detail(request, pk):
    data = cartData(request)
    cartItems =data['cartItems']
    products = Product.objects.all()
    products = Product.objects.get(id=pk)
    items = data['items']
    context = {'products':products, 'items':items, 'cartItems':cartItems}
   
    return render(request, 'store/detail.html', context)

def checkout(request):

   
    data = cartData(request)
    cartItems =data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print("Action:", action)
    print("productId:", productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem,created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added',safe=False)

# def processOrder(request):
# 	transaction_id = datetime.datetime.now().timestamp()
# 	data = json.loads(request.body)

# 	if request.user.is_authenticated:
# 		customer = request.user.customer
# 		order, created = Order.objects.get_or_create(customer=customer, complete=False)
# 	else:
# 		customer, order = guestOrder(request, data)

# 	total = float(data['form']['total'])
# 	order.transaction_id = transaction_id

# 	if total == order.get_cart_total:
# 		order.complete = True
# 	order.save()

# 	if order.shipping == True:
# 		ShippingAddress.objects.create(
# 		customer=customer,
# 		order=order,
# 		address=data['shipping']['address'],
# 		city=data['shipping']['city'],
# 		state=data['shipping']['state'],
# 		zipcode=data['shipping']['zipcode'],
# 		)

# 	return JsonResponse('Payment submitted..', safe=False)