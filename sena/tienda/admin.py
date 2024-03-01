from django.contrib import admin
from django.utils.html import mark_safe
from .models import *

# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
	list_display = ["id", "nombre", "descripcion"]
	search_fields = ["nombre"]


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
	list_display = ["id", "nombre", "precio", "inventario", "fecha_creacion", "categoria", 'foto', 'ver_foto']
	search_fields = ["nombre"]
	list_filter = ["categoria", "fecha_creacion"]
	list_editable = ["categoria"]

	def ver_foto(self, obj):
		return mark_safe(f"<a href='{obj.foto.url}'><img src='{obj.foto.url}' width='25%'></a>")


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
	list_display = ['id', 'nombre', 'nombre_en_plural', 'correo', 'clave', 'rol', 'foto', 'ver_foto']

	def nombre_en_plural(self, obj):
		return mark_safe(f"<span style='color:red'>{obj.nombre}'s<span>")

	def ver_foto(self, obj):
		return mark_safe(f"<a href='{obj.foto.url}'><img src='{obj.foto.url}' width='15%'></a>")

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha_venta', 'usuario']

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'venta', 'producto', 'cantidad', 'precio_historico', 'subtotal', 'fecha_compra']

    def subtotal(self, obj):
        return f"{obj.cantidad * obj.precio_historico}"

    def fecha_compra(self, obj):
        return obj.venta.fecha_venta

    fecha_compra.short_description = "Fecha de compra"