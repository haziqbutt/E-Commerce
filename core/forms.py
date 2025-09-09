# core/forms.py
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import City  # City has (name, country)

# Inline choices (no constants.py required)
PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
)

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 Main St',
        'class': 'form-control',
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or suite',
        'class': 'form-control',
    }))

    # Explicit ids so your template JS can select them easily
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
            'id': 'country',
        })
    )

    city = forms.ModelChoiceField(
        queryset=City.objects.none(),
        widget=forms.Select(attrs={
            'class': 'custom-select d-block w-100',
            'id': 'city',
        }),
        required=True,
    )

    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On POST, populate city choices based on selected country (ISO code like "PK")
        country_code = (self.data.get('country') or self.initial.get('country') or '').strip()
        if country_code:
            self.fields['city'].queryset = City.objects.filter(country=country_code).order_by('name')
        else:
            self.fields['city'].queryset = City.objects.none()


class CouponForm(forms.Form):
    code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter coupon code',
            'aria-label': 'Coupon code',
        })
    )


class RefundForm(forms.Form):
    # Minimal stub; adjust to your needs if you use a refund page
    ref_code = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Order reference code'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Describe the issue'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'})
    )
