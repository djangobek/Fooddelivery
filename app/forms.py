from django import forms
from .models import OrderTable, OrderTableItem

class OrderTableForm(forms.ModelForm):
    class Meta:
        model = OrderTable
        fields = ['name', 'status']

class OrderTableItemForm(forms.ModelForm):
    class Meta:
        model = OrderTableItem
        fields = ['product', 'quantity']