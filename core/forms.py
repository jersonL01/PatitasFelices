from django import forms
from django.forms import ModelForm
from .models import *


# ES EL TEMPLATE DEL FORMULARIO
class ProductoForm(ModelForm):

    nombre = forms.CharField(min_length=4,widget=forms.TextInput(attrs={"placeholder":"Ingrese Nombre"}))
    precio = forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={"placeholder":"Ingrese Precio"}))
    stock = forms.IntegerField(min_value=0,widget=forms.NumberInput(attrs={"placeholder":"Ingrese Stock"}))
    descripcion = forms.CharField(min_length=10,max_length=200,widget=forms.Textarea(attrs={"rows":4}))

    class  Meta :
        model = Producto
        fields= '__all__'

            
        widgets = {
                'vencimiento' : forms.SelectDateWidget(years=range(2023,2031))
            }





