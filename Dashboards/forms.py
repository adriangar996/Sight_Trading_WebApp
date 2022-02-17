from django import forms


class SearchStockForm(forms.Form):
    search_stock = forms.CharField(label='search_stock', max_length=10)
    


