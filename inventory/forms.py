from django import forms
from .models import Inventory
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Kullanıcı Adı", widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Şifre", widget=forms.PasswordInput())

class AddInventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'cost_per_item', 'quantity_in_stock', 'quantity_sold']
        widgets = {
            'cost_per_item': forms.NumberInput(attrs={'min': 0}),
            'quantity_in_stock': forms.NumberInput(attrs={'min': 0}),
            'quantity_sold': forms.NumberInput(attrs={'min': 0}),
        }
        labels = {
            'name': 'Ürün Adı',
            'cost_per_item': 'Birim Maliyeti',
            'quantity_in_stock': 'Stok Miktarı',
            'quantity_sold': 'Satılan Miktar',
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity_in_stock = cleaned_data.get('quantity_in_stock')
        quantity_sold = cleaned_data.get('quantity_sold')

        if quantity_sold > quantity_in_stock:
            raise forms.ValidationError("Satılan miktar, stok miktarından fazla olamaz.")

class UpdateInventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'cost_per_item', 'quantity_in_stock', 'quantity_sold']
        widgets = {
            'cost_per_item': forms.NumberInput(attrs={'min': 0}),
            'quantity_in_stock': forms.NumberInput(attrs={'min': 0}),
            'quantity_sold': forms.NumberInput(attrs={'min': 0}),
        }
        labels = {
            'name': 'Ürün Adı',
            'cost_per_item': 'Birim Maliyeti',
            'quantity_in_stock': 'Stok Miktarı',
            'quantity_sold': 'Satılan Miktar',
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity_in_stock = cleaned_data.get('quantity_in_stock')
        quantity_sold = cleaned_data.get('quantity_sold')

        if quantity_sold > quantity_in_stock:
            raise forms.ValidationError("Satılan miktar, stok miktarından fazla olamaz.")
        from django import forms
from django.contrib.auth.forms import AuthenticationForm

