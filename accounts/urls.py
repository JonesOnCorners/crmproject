from django.urls import path
import accounts.views as views



urlpatterns = [
    path('',views.home, name='index'),
    path('products',views.products, name='products'),
    path('customer/<str:pk>/',views.customer, name='customer'),
    path('createorder/<str:pk>/',views.createOrder, name='create_order'),
    path('updateorder/<str:pk>/',views.updateOrder, name='update_order'),
    path('deleteorder/<str:pk>/',views.deleteOrder, name='delete_order'),
    path('createcustomer',views.createCustomer, name='create_customer'),
    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('register',views.register, name='register'),
    path('user',views.userPage, name='user'),
    path('accountsettings',views.accountSettings, name='account_setting'),
]