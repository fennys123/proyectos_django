from rest_framework import serializers

from .models import *

# Serializers define the API representation.


class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre_cat', 'desc']


class PeliculaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pelicula
        fields = ['id', 'titulo', 'categoria', 'estreno', 'imagen', 'resumen', 'favoritos']

