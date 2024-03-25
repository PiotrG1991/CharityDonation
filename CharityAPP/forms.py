from django import forms

from CharityAPP.models import Donation


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = '__all__'