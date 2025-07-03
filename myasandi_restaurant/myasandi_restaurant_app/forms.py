from django import forms
from .models import *

class MenuModelForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['itemPhoto', 'menuName', 'price', 'categoryName','kitchenName', 'out_of_order']
        widgets = {
            'itemPhoto': forms.ClearableFileInput(attrs= {'class':'form-control'}),
             'menuName': forms.TextInput(attrs={'class':'form-control'}),
             'price' : forms.NumberInput(attrs = {'class': 'form-control'}),
             'categoryName': forms.Select(attrs={'class':'form-control'}),
             'kitchenName': forms.Select(attrs={'class':'form-control'}),
             'out_of_order': forms.CheckboxInput(attrs={'class':'form-check-input','type':'checkbox'})
        }
class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['categoryName','menuPhoto']
        widgets = {
            'categoryName': forms.TextInput(attrs={'class':'form-control'}),
            'menuPhoto': forms.ClearableFileInput(attrs= {'class':'form-control'}),             
        }

# accounts/forms.py


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'
    }))
