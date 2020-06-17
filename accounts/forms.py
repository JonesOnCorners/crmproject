from django.forms import ModelForm, FileInput
from accounts.models import Order, Customer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'porfile_pic': FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['porfile_pic'].widget.attrs = {'id':'selectedFile'} 


class CreateUserForm(UserCreationForm):
    class Meta:
        model  = User
        fields = ['username','email','password1','password2']