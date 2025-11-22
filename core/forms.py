from django import forms 
from core.models import CreditCard

class CreditCardForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Card Holder's Name"}))
    card_number = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder": "Card Number"}))
    cvc = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder":"CVC/CVV"}))
    month = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder":"MM (e.g., 08)"}))
    year = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder":"YY (e.g., 24)"}))
    card_type = forms.ChoiceField(choices=[('master', 'Master'), ('visa', 'Visa'), ('verve', 'Verve')], widget=forms.Select(attrs={"class": "form-control custom-select"}))

    class Meta: 
        model = CreditCard
        fields = ["name", "card_number", "cvc", "month", "year", "card_type",]

