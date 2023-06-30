
from email.policy import HTTP
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from rest_framework import viewsets
from .serializers import *
import requests
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models import Sum, F , Q
from .carrito import *
from django.shortcuts import render,redirect,get_object_or_404




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

    productos = Producto.objects.all()

    return render(request, 'core/cart.html')

    # LOGICA DEL CARRITO, SE SUMAN TODOS LOS PRECIOS
    """
    respuesta = requests.get('https://mindicador.cl/api/dolar').json()
    valor_usd = respuesta['serie'][0]['valor']

    items_carrito = Carrito.objects.filter(usuario=request.user)
    cantidad_total = items_carrito.aggregate(total_cantidad=Sum('cantidad'))
    cantidad_seleccionada = request.GET.get('cantidad')
    
    
    precio_total = items_carrito.annotate(precio_total=F('producto__precio') * F('cantidad')).aggregate(total_precio=Sum('precio_total'))
    if precio_total['total_precio'] is not None and valor_usd != 0:
        precio_total = round(precio_total['total_precio'] / valor_usd,2)
    else:
        precio_total = 0
    
    return render(request, 'core/cart.html', {
        'items_carrito': items_carrito,
        'cantidad_total': cantidad_total['total_cantidad'],
        'precio_total': precio_total,
        'cantidad_seleccionada': cantidad_seleccionada,
    })"""


def checkout(request):
    return render(request, 'core/checkout.html')

def contact(request):
    return render(request, 'core/contact.html')
    
def productsingle(request):
    return render(request, 'core/productsingle.html')
    
def shopAdmin(request):
    productosAll= Producto.objects.all()
    data={

        'listaProductos': productosAll
    }

    return render(request, 'core/shopAdmin.html',data)
    
def shop(request):
    productosAll= Producto.objects.all()
    data={

        'listaProductos': productosAll
    }

    return render(request, 'core/shop.html',data)
def register(request):

    return render(request, 'registration/register.html')
       

def seguimiento(request):
    return render(request, 'core/seguimiento.html')

def suscripcion(request):
    return render(request, 'core/suscripcion.html')
# SHOP API
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

# CARRITO

def agregaralcarrito(request, id):
    producto = Producto.objects.get(id=id)
    
    # Verificar si el stock es cero
    if producto.stock == 0:
        messages.error(request, 'Hay un producto agotado en tu carrito.')
    else:
        item_carrito, created = Cart.objects.get_or_create(
            producto=producto,
            usuario=request.user,
            defaults={'cantidad': 1}
        )
        if not created:
            item_carrito.cantidad += 1
            item_carrito.save()
        
        # Restar la cantidad del producto al stock disponible
        Producto.objects.filter(id=id).update(stock=F('stock') - 1)
        
    total_precio = Cart.objects.filter(usuario=request.user).aggregate(Sum('producto__precio'))
    request.session['total_precio'] = total_precio.get('producto__precio__sum', 0)
    
    return redirect('cart')

def comprar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    if producto.stock > 0:
        producto.stock -= 1
        producto.save()
        
    return redirect("cart")    


def devolvercarrito(request):
    items_carrito = Cart.objects.filter(usuario=request.user)
    
    # Devolver la cantidad de productos al stock disponible
    for item in items_carrito:
        Producto.objects.filter(id=item.producto.id).update(stock=F('stock') + item.cantidad)
    
    # Eliminar todos los productos del carrito
    items_carrito.delete()
    
    return redirect('cart')


def eliminarcarrito(request, id):
    carrito = Cart(request)
    producto = Producto.objects.get(id=id)
    carrito.restar(producto)
    return redirect("cart")



def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)
    Cart.objects.filter(producto=producto, usuario=request.user).delete()
    return redirect("cart")


def agregaralcarrito(request, id):
    producto = Producto.objects.get(id=id)
    
    # Verificar si el stock es cero
    if producto.stock == 0:
        messages.error(request, 'Hay un producto agotado en tu carrito.')
    else:
        item_carrito, created = Cart.objects.get_or_create(
            producto=producto,
            usuario=request.user,
            defaults={'cantidad': 1}
        )
        if not created:
            item_carrito.cantidad += 1
            item_carrito.save()
        
        # Restar la cantidad del producto al stock disponible
        Producto.objects.filter(id=id).update(stock=F('stock') - 1)
        
    total_precio = Cart.objects.filter(usuario=request.user).aggregate(Sum('producto__precio'))
    request.session['total_precio'] = total_precio.get('producto__precio__sum', 0)
    
    return redirect('cart')


def restar_producto(request, id):
    item_carrito = Cart.objects.get(producto__id=id, usuario=request.user)
    
    if item_carrito.cantidad > 1:
        item_carrito.cantidad -= 1
        Producto.objects.filter(id=item_carrito.producto.id).update(stock=F('stock') + 1)
        item_carrito.save()
    else:
        # Devolver la cantidad del producto al stock disponible
        Producto.objects.filter(id=item_carrito.producto.id).update(stock=F('stock') + 1)
        item_carrito.delete()

    return redirect("cart")


def limpiar_carrito(request):
    Cart.objects.filter(usuario=request.user).delete()
    request.session['total_precio'] = 0
    return redirect("cart")


