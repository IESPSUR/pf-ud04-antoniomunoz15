from django.core.exceptions import ValidationError
from django import forms
from .models import Producto

class F_prod(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'