from django import forms
from .models import ShippingAddress


class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    shipping_email = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    shipping_address1 = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address1'}))
    shipping_address2 = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address2'}))
    shipping_city = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    shipping_state = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    shipping_zipcode = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}))
    shipping_country = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}))

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country']

        exclude = ['user',]
