from django.contrib import admin
from .models import *
# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre','precio','stock','descripcion','tipo']
    search_fields = ['nombre']
    list_per_page = 10
    list_editable = ['precio','stock','descripcion','tipo']
    list_filter = ['tipo', 'stock']

admin.site.register(TipoProducto)
admin.site.register(Producto, ProductoAdmin)





 