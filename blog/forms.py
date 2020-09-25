from django.forms import ModelForm
from .models import Value


class ValueForm(ModelForm):
    class Meta:
        model = Value
        fields = ['temperature', 'ph']