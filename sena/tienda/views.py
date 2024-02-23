from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DetalleVenta, Producto, Venta

# Importamos todos los modelos de la base de datos
from .models import *

# Create your views here.

def index(request):
	logueo = request.session.get("logueo", False)

	if logueo == False:
		return render(request, "tienda/login/login.html")
	else:
		return redirect("inicio")


def login(request):
	if request.method == "POST":
		user = request.POST.get("correo")
		passw = request.POST.get("clave")
		# select * from Usuario where correo = "user" and clave = "passw"
		try:
			q = Usuario.objects.get(correo=user, clave=passw)
			# Crear variable de sesión
			request.session["logueo"] = {
				"id": q.id,
				"nombre": q.nombre,
				"rol": q.rol,
				"nombre_rol": q.get_rol_display()
			}
			request.session["carrito"] = []
			request.session["items"] = 0
			messages.success(request, f"Bienvenido {q.nombre}!!")
			return redirect("inicio")
		except Exception as e:
			messages.error(request, "Error: Usuario o contraseña incorrectos...")
			return redirect("index")
	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("index")


def logout(request):
	try:
		del request.session["logueo"]
		del request.session["carrito"]
		del request.session["items"]
		messages.success(request, "Sesión cerrada correctamente!")
		return redirect("index")
	except Exception as e:
		messages.warning(request, "No se pudo cerrar sesión...")
		return redirect("inicio")


def inicio(request):
	logueo = request.session.get("logueo", False)

	if logueo:
		categorias = Categoria.objects.all()

		cat = request.GET.get("cat")
		if cat == None:
			productos = Producto.objects.all()
		else:
			c = Categoria.objects.get(pk=cat)
			productos = Producto.objects.filter(categoria=c)

		contexto = {"data": productos, "cat": categorias}
		return render(request, "tienda/inicio.html", contexto)
	else:
		return redirect("index")


from .decorador_especial import *


@login_requerido
def categorias(request):
	q = Categoria.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/categorias/categorias.html", contexto)



def categorias_form(request):
	return render(request, "tienda/categorias/categorias_form.html")


def categorias_crear(request):
	if request.method == "POST":
		nomb = request.POST.get("nombre")
		desc = request.POST.get("descripcion")
		try:
			q = Categoria(
				nombre=nomb,
				descripcion=desc
			)
			q.save()
			messages.success(request, "Guardado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
		return redirect("categorias_listar")

	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("categorias_listar")


def categorias_eliminar(request, id):
	try:
		q = Categoria.objects.get(pk=id)
		q.delete()
		messages.success(request, "Categoría eliminada correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")

	return redirect("categorias_listar")


def categorias_formulario_editar(request, id):
	q = Categoria.objects.get(pk=id)
	contexto = {"data": q}
	return render(request, "tienda/categorias/categorias_formulario_editar.html", contexto)

def categorias_actualizar(request):
	if request.method == "POST":
		id = request.POST.get("id")
		nomb = request.POST.get("nombre")
		desc = request.POST.get("descripcion")
		try:
			q = Categoria.objects.get(pk=id)
			q.nombre = nomb
			q.descripcion = desc
			q.save()
			messages.success(request, "Categoría actualizada correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
	else:
		messages.warning(request, "Error: No se enviaron datos...")

	return redirect("categorias_listar")


@login_requerido
def productos(request):
	q = Producto.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/productos/productos.html", contexto)


def productos_form(request):
	q = Categoria.objects.all()
	contexto = {"data": q}
	return render(request, "tienda/productos/productos_form.html", contexto)


def productos_crear(request):
	if request.method == "POST":
		nombre = request.POST.get("nombre")
		precio = request.POST.get("precio")
		inventario = request.POST.get("inventario")
		fecha_creacion = request.POST.get("fecha_creacion")
		categoria = Categoria.objects.get(pk=request.POST.get("categoria"))
		try:
			q = Producto(
				nombre=nombre,
				precio=precio,
				inventario=inventario,
				fecha_creacion=fecha_creacion,
				categoria=categoria
			)
			q.save()
			messages.success(request, "Guardado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
		return redirect("productos_listar")

	else:
		messages.warning(request, "Error: No se enviaron datos...")
		return redirect("productos_listar")


def productos_eliminar(request, id):
	try:
		q = Producto.objects.get(pk=id)
		q.delete()
		messages.success(request, "Producto eliminada correctamente!!")
	except Exception as e:
		messages.error(request, f"Error: {e}")

	return redirect("productos_listar")


def productos_formulario_editar(request, id):
	q = Producto.objects.get(pk=id)
	c = Categoria.objects.all()
	contexto = {"data": q, "categoria": c}
	return render(request, "tienda/productos/productos_formulario_editar.html", contexto)

def productos_actualizar(request):
	if request.method == "POST":
		id = request.POST.get("id")
		nombre = request.POST.get("nombre")
		precio = request.POST.get("precio")
		inventario = request.POST.get("inventario")
		fecha_creacion = request.POST.get("fecha_creacion")
		categoria = Categoria.objects.get(pk=request.POST.get("categoria"))
		try:
			q = Producto.objects.get(pk=id)
			q.nombre = nombre
			q.precio = precio
			q.inventario = inventario
			q.fecha_creacion = fecha_creacion
			q.categoria = categoria
			q.save()
			messages.success(request, "Producto actualizado correctamente!!")
		except Exception as e:
			messages.error(request, f"Error: {e}")
	else:
		messages.warning(request, "Error: No se enviaron datos...")

	return redirect("productos_listar")


def ver_perfil(request):
	logueo = request.session.get("logueo", False)
	# Consultamos en DB por el ID del usuario logueado....
	q = Usuario.objects.get(pk=logueo["id"])
	contexto = {"data": q}
	return render(request, "tienda/login/perfil.html", contexto)


def cambio_clave_formulario(request):
	return render(request, "tienda/login/cambio_clave.html")


def cambiar_clave(request):
	if request.method == "POST":
		logueo = request.session.get("logueo", False)
		q = Usuario.objects.get(pk=logueo["id"])

		c1 = request.POST.get("nueva1")
		c2 = request.POST.get("nueva2")

		if q.clave == request.POST.get("clave"):
			if c1 == c2:
				# cambiar clave en DB
				q.clave = c1
				q.save()
				messages.success(request, "Contraseña guardada correctamente!!")
			else:
				messages.info(request, "Las contraseñas nuevas no coinciden...")
		else:
			messages.error(request, "Contraseña no válida...")
	else:
		messages.warning(request, "Error: No se enviaron datos...")

	return redirect('cc_formulario')


def carrito_add(request):
	if request.method == "POST":
		try:
			carrito = request.session.get("carrito", False)
			if not carrito:
				request.session["carrito"] = []
				request.session["items"] = 0
				carrito = []

			id_producto = int(request.POST.get("id"))
			cantidad = request.POST.get("cantidad")
			# Consulto el producto en DB...........................
			q = Producto.objects.get(pk=id_producto)
			for p in carrito:
				if p["id"] == id_producto:
					if q.inventario >= (p["cantidad"] + int(cantidad)) and int(cantidad) > 0:
						p["cantidad"] += int(cantidad)
						p["subtotal"] = p["cantidad"] * q.precio
					else:
						print("Cantidad supera inventario...")
						messages.warning(request, "Cantidad supera inventario...")
					break
			else:
				print("No existe en carrito... lo agregamos")
				if q.inventario >= int(cantidad) and int(cantidad) > 0:
					carrito.append(
						{
							"id": q.id,
							"foto": q.foto.url,
							"producto": q.nombre,
							"precio": q.precio,
							"cantidad": int(cantidad),
							"subtotal": int(cantidad) * q.precio
						}
					)
				else:
					print("Cantidad supera inventario...")
					messages.warning(request, "No se puede agregar, no hay suficiente inventario.")

			# Actualizamos variable de sesión carrito...
			request.session["carrito"] = carrito

			contexto = {
				"items": len(carrito),
				"total": sum(p["subtotal"] for p in carrito)
			}
			request.session["items"] = len(carrito)

			return render(request, "tienda/carrito/carrito.html", contexto)
		except ValueError as e:
			messages.error(request, f"Error: Digite un valor correcto para cantidad")
			return HttpResponse("Error")
		except Exception as e:
			messages.error(request, f"Ocurrió un Error: {e}")
			return HttpResponse("Error")
	else:
		messages.warning(request, "No se enviaron datos.")
		return HttpResponse("Error")


def carrito_ver(request):
	carrito = request.session.get("carrito", False)
	if not carrito:
		request.session["carrito"] = []
		request.session["items"] = 0
		contexto = {
			"items": 0,
			"total": 0
		}
	else:
		contexto = {
			"items": len(carrito),
			"total": sum(p["subtotal"] for p in carrito)
		}
		request.session["items"] = len(carrito)

	return render(request, "tienda/carrito/carrito.html", contexto)


def vaciar_carrito(request):
	request.session["carrito"] = []
	request.session["items"] = 0
	return redirect("inicio")

def eliminar_item_carrito(request, id_producto):
	carrito = request.session.get("carrito", False)
	if carrito != False:
		for i,item in enumerate(carrito):
			if item["id"] == id_producto:
				carrito.pop(i)
				break
		else:
			messages.warning(request, "No se encontro el item en el carrito...")
	
	request.session["items"] = len(carrito)
	request.session["carrito"] = carrito
	return redirect("carrito_ver")

def actualizar_totales_carrito(request,id_producto):
	carrito = request.session.get("carrito", False)
	cantidad = request.GET.get("cantidad")


	if carrito != False:
		for i,item in enumerate(carrito):
			if item["id"] == id_producto:
				item["cantidad"] = int(cantidad)
				item["subtotal"] = int(cantidad) * item["precio"]
				break
		else:
			messages.warning(request, "No se encontro el item en el carrito...")
	
	request.session["items"] = len(carrito)
	request.session["carrito"] = carrito
	return redirect("inicio")

@receiver(post_save, sender=Venta)
def actualizar_inventario(sender, instance, created, **kwargs):
    if created:
        carrito = instance.detalles.all()
        for item in carrito:
            producto = item.producto
            producto.inventario -= item.cantidad
            producto.save()

def pagar_carrito(request):
    if request.method == 'POST':
        # Obtén los datos del pedido desde la solicitud HTTP del webhook
        order_id = request.POST.get('order_id')
        # Crea una nueva venta en la base de datos
        usuario = request.user
        venta = Venta.objects.create(usuario=usuario, estado=1)  # Estado "Pendiente"
        # Crea los detalles de la venta en la base de datos
        carrito = request.session.get("carrito", [])
        for item in carrito:
            producto = Producto.objects.get(id=item["id"])
            detalle_venta = DetalleVenta.objects.create(venta=venta, producto=producto, cantidad=item["cantidad"], precio_historico=producto.precio)
        # Vacía el carrito de la sesión
        request.session["carrito"] = []
        request.session["items"] = 0
        # Actualiza el inventario de los productos
        actualizar_inventario(sender=None, instance=venta, created=True)
        # Muestra un mensaje de éxito y redirige al usuario a la página de inicio
        messages.success(request, "¡Gracias por su compra!")
        return redirect("inicio")
    else:
        messages.warning(request, "Error: No se enviaron datos...")
        return redirect("inicio")