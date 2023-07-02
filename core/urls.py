from django.urls import path, include
from .views import *
from rest_framework import routers

# RUTAS DEL API
router = routers.DefaultRouter()
router.register('productos', ProductoViewset)

urlpatterns = [

    # API

    path('api/', include(router.urls)),
   

    # RUTAS
    path('', index, name="index" ),
    path('about/', about, name="about" ),
    path('cart/', cart, name="cart" ),
    path('checkout/', checkout, name="checkout" ),
    path('contact/', contact, name="contact" ),
    path('productsingle/', productsingle, name="productsingle" ),
    path('shopAdmin/', shopAdmin, name="shopAdmin" ),
    path('UniversoApi/', UniversoApi, name="UniversoApi" ),
    path('register/', register, name="register" ),
    path('seguimiento/', seguimiento, name="seguimiento"),
    path('shop/', shop, name="shop"),
    path('suscripcion/', suscripcion, name="suscripcion"),



    # CRUD

    path('agregarproductos/', agregarproductos, name="agregarproductos" ),
    path('actualizarproductos/<id>/', actualizarproductos, name="actualizarproductos" ),
    path('eliminar/<id>/', eliminar, name="eliminar" ),





    
    # CARRITO

    path('eliminar/<id>/', eliminar_producto, name="Del"),
    path('restar/<id>/', restar_producto, name="Sub"),
    path('limpiar/', limpiar_carrito, name="CLS"),
    path('agregar/<id>/', agregaralcarrito, name="Add"),
    path('comprar_producto/<id>/', comprar_producto, name='comprar_producto'),
    path('devolvercarrito/', devolvercarrito, name="devolvercarrito"),
    path('agregaralcarrito/<id>/', agregaralcarrito, name="agregaralcarrito"),
    path('eliminarcarrito/<id>/', eliminarcarrito, name="eliminarcarrito"),













]



