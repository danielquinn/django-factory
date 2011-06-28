from django import forms
from core.models import Factory

class FactoryForm(forms.ModelForm):
    """
        Subclass this form for any ModelForm that's also a child of Factory.
    """

    class Meta:
        model = Factory
        exlude = ("_factorypath",)

