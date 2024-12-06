from django import forms
from .models import Billing


class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['first_name', 'last_name', 'address', 'city', 'postal_code', 'country', 'phone', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Last Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'In which city do you reside?'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Postal Code'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Country'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Email'}),
        }


from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['card_number', 'card_holder', 'expiration_date', 'cvv', 'billing_address']

        widgets = {
            'card_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Number'}),
            'card_holder': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Holder Name'}),
            'expiration_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'}),
            'cvv': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVV'}),
            'billing_address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Billing Address'}),
        }

from django import forms
from visitor.models import NewUser

class MpesaForm(forms.Form):
    phone_number = forms.CharField(max_length=13, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    account_reference = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account Reference'}))
    transaction_desc = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Transaction Description'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['phone_number'].initial = user.profile.phone
            self.fields['account_reference'].initial = f'Payment-{user.id}'
            self.fields['transaction_desc'].initial = f'Payment for user {user.email}'
