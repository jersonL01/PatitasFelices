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
    path('shop/', shop, name="shop" ),
    path('shopApi/', shopApi, name="shopApi" ),

    
    # CRUD

    path('agregarproductos/', agregarproductos, name="agregarproductos" ),
    path('actualizarproductos/<id>/', actualizarproductos, name="actualizarproductos" ),
    path('eliminar/<id>/', eliminar, name="eliminar" ),
]
