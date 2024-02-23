from django.db import models


# Create your models here.
class Categoria(models.Model):
	nombre_cat = models.CharField(max_length=150)
	desc = models.TextField(help_text="Descripción corta de la categoría")

	def __str__(self):
		return f"{self.nombre_cat}"


class Pelicula(models.Model):
	categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
	titulo = models.CharField(max_length=150)
	estreno = models.IntegerField(default=2000)
	imagen = models.URLField(help_text="De imdb mismo")
	resumen = models.TextField(help_text="Descripción corta")
	favoritos = models.IntegerField(default=0)
	fecha_created = models.DateTimeField(auto_now_add=True, blank=True)
	fecha_updated = models.DateTimeField(auto_now=True, blank=True)

	def __str__(self):
		return f"{self.titulo}"

	class Meta:
		ordering = ['titulo']

