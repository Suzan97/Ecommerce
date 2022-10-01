from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.store, name= "index"),
    path('cust_signup/', views.customer_register.as_view(), name = "cust_signup"),
    path('comp_signup/', views.vendor_register.as_view(), name = "comp_signup"),
    # path('signup/', views.signup, name = "signup"),
    # path('comp_signup/', views.comp_signup, name = "comp_signup"),
    path('home/', views.home, name = "home"),
    path('cart/', views.cart, name= "cart"),
    path('checkout/', views.checkout, name= "checkout"),
    path('shop/', views.shop, name= "shop" ),
    path('detail/', views.detail, name = "detail"),
    path('detail/<str:pk>/',views.detail, name='detail'),
    # path('customer_register/', views.student_register.as_view(), name='student_register'),
    # path('vendor_register/', views.teacher_register.as_view(), name='teacher_register'),
    # path('logout/', views.logout_user, name='logout_user'),


    path('update_item/', views.updateItem, name="update_item"),

]