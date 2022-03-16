from django import forms

class AddStockForm(forms.Form):
    add_stock = forms.CharField(label='add_stock', max_length=10)
    stocks_bought = forms.IntegerField(label='stocks_bought')
    buying_price = forms.DecimalField(label='buying_price', min_value=0)

class AddWatchlistForm(forms.Form):
    add_stock = forms.CharField(label='add_stock', max_length=10)

class SelectedStockForm(forms.Form):
    selected_stock = forms.CharField(label='selected_stock', max_length=10)

# class ChangePasswordForm(forms.Form):
#     password_change = forms.CharField(widget={'change_password':forms.PasswordInput()})

class ChangeEmailForm(forms.Form):
    email_change = forms.EmailField(label='change_email')

class RemoveStockForm(forms.Form):
    remove_stock = forms.CharField(label='remove_stock')