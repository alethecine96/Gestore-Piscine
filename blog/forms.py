from django.forms import ModelForm
from django import forms
from .models import Value


class PiscinaForm(forms.Form):
    temperature = forms.CharField()
"""
    class Meta:
        model = Value
        fields = ['temperature',]
"""