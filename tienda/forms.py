from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['marca',]

class CompraForm(forms.Form):
    unidades = forms.IntegerField(min_value=1)

