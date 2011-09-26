from django import forms
from django_factory.models import Factory

class FactoryForm(forms.ModelForm):
    """
        Subclass this form for any ModelForm that's also a child of Factory.
    """

    class Meta:
        model = Factory
        exclude = ("_factorypath",)
