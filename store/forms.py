from django import forms
from .models import Comment, Customer, Order
from django.utils.translation import gettext_lazy as _


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'text', 'stars']
    

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone_number', 'address', 'email' ]


def is_color(color):
    return color

class AddProductToCartForm(forms.Form):
    QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 31)]
    quantity = forms.TypedChoiceField(choices=QUANTITY_CHOICES, coerce=int,)
    color = forms.CharField(max_length=20, required=True, )
    size = forms.CharField(max_length=20)
    inplace = forms.BooleanField(required=False, widget=forms.HiddenInput)
    

class OrderRegisterForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={"required": True, "class": "form-control", 'name': 'first_name', 'id':'first_name', 'placeholder': _("First Name*")}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"required": True, "class": "form-control", 'name': 'last_name', 'id':'last_name', 'placeholder': _("Last Name*")}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={"required": True, "class": "form-control", 'name': 'phone_number', 'id':'phone_number', 'placeholder': _("Phone Number*")}))
    address = forms.CharField(widget=forms.TextInput(attrs={"required": True, "class": "form-control", 'name': 'address', 'id':'address', 'placeholder': _("Full Address*")}))
    order_note = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", 'name': 'order_note', 'id':'order_note', 'cols': "30", 'rows': '5', 'placeholder': _("Order Note")}), required=False)

    class Meta:
        model = Order
        fields = ['first_name','last_name','phone_number','address','order_note']

