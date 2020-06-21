from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length = 250, null=True)
    phone = models.CharField(max_length = 250, null=True)
    email = models.EmailField(max_length= 250, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    porfile_pic = models.ImageField(null=True,default="logo.png",blank=True)

    def __str__(self):
        return self.user.username

class Product(models.Model):
    CATEGORY=(
        ('Indoor','Indoor'),
        ('Outdoor','Outdoor'),
    )
    name = models.CharField(max_length= 250, null=True)
    price = models.FloatField(null=True)
    category= models.CharField(max_length=250,null=True, choices=CATEGORY)
    date_created = models.DateTimeField(auto_now_add=True,null=True)    

    def __str__(self):
        return self.name



class Order(models.Model):
    STATUS=(
        ('Pending','Pending'),
        ('Out For Delivery','Out For Delivery'),
        ('Delivered','Delivered'),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=250, null=True, choices=STATUS)
    
    def __str__(self):
        return str(self.product)