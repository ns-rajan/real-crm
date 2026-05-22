from django import forms

from locations.models import Country
from crm.models import Request


class PublicRequestForm(forms.ModelForm):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        label="Country",
    )

    class Meta:
        model = Request
        fields = [
            "request_for",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "phone",
            "company_name",
            "country",
            "city_name",
            "description",
        ]


