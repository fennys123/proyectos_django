from django.http import HttpResponse
from django.shortcuts import render

from .models import *
from .serializers import *
from rest_framework import viewsets


# Create your views here.
def index(request):
	return HttpResponse("Hola mundo Django-Rest.")

# Vistas para el conjunto de datos de la API
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class PeliculaViewSet(viewsets.ModelViewSet):
    queryset = Pelicula.objects.all()
    serializer_class = PeliculaSerializer
