from django.forms import ModelForm
from .models import Value


class PiscinaForm(ModelForm):
    class Meta:
        model = Value
        fields = ['temperature', 'ph']