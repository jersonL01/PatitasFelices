from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from rest_framework import viewsets
from .serializers import *
import requests
from django.contrib.auth.decorators import login_required, user_passes_test


# FUNCION GENERICA QUE VALIDA EL GRUPO DEL USUARIO
def grupo_requerido(nombre_grupo):
    def decorator(view_fuc):
        @user_passes_test(lambda user: user.groups.filter(name=nombre_grupo).exists())
        def wrapper(request, *arg, **kwargs):
            return view_fuc(request, *arg, **kwargs)
        return wrapper
    return decorator

# @grupo_requerido('nombre del grupo : admin, cliente, vendedor')
# CUANDO CREAN EL USUARIO LO ASIGNA INMEDIATAMENTE AL GRUPO
# grupo = Group.objects.get(name='cliente')
# user.groups.add(grupo)


# SE ENCARGA DE MOSTRAR EN LA VISTA LOS DATOS
class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def about(request):
    return render(request, 'core/about.html')

def cart(request):
    # LOGICA DEL CARRITO, SE SUMAN TODOS LOS PRECIOS

    respuesta_usd = requests.get('https://mindicador.cl/api/dolar').json()
    valor_usd = respuesta_usd['serie'][0]['valor']
    valor_carrito = 30000 # SE SUPONER QUE ES EL TOTAL DEL CARRITO
    valor_total = valor_carrito/valor_usd

    data ={
        'valor' : round(valor_total,2)
    }
    return render(request, 'core/cart.html',data)

def checkout(request):
    return render(request, 'core/checkout.html')

def contact(request):
    return render(request, 'core/contact.html')
    
def productsingle(request):
    return render(request, 'core/productsingle.html')
    
def shop(request):
    productosAll= Producto.objects.all()
    data={

        'listaProductos': productosAll
    }

    return render(request, 'core/shop.html',data)

# API VIEW
def shopApi(request):
    # REALIZAMOS LA SOLICITUD AL API
    respuesta = requests.get('http://127.0.0.1:8000/api/productos/')
    respuesta2 = requests.get('https://mindicador.cl/api/')
    respuesta3 = requests.get('https://rickandmortyapi.com/api/character')
    respuesta4 = requests.get('https://digimon-api.vercel.app/api/digimon')

    # TRANSFORMAMOS ELJSON PARA LEERLO

    productos = respuesta.json()
    monedas = respuesta2.json()
    aux = respuesta3.json()
    personajes = aux['results']
    digimon = respuesta4.json()

    data={

        'listaProductos': productos,
        'monedas' : monedas,
        'personajes' : personajes,
        'digimon' : digimon,
    }

    return render(request, 'core/shopApi.html',data)


#CRUD

def agregarproductos(request):
    data={

       'form' : ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES) # RECIBE EL CONTENIDO DEL FORMULARIO

        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto almacenado correctamente")
            
    return render(request, 'core/agregarproductos.html', data)

def actualizarproductos(request, id):
    producto = Producto.objects.get(id=id)
    data={

       'form' : ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES ) # RECIBE EL CONTENIDO DEL FORMULARIO

        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto actualizado correctamente")
        data['form'] = formulario
            
    return render(request, 'core/actualizarproductos.html', data)

def eliminar(request, id):
    producto = Producto.objects.get(id=id)
    producto.eliminar()

    return redirect( to="shop")
