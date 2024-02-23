from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from . import views


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'categoria', views.CategoriaViewSet)
router.register(r'pelicula', views.PeliculaViewSet)

urlpatterns = [
	path("", views.index, name="index"),
	path("api/1.0/", include(router.urls)),
	path('docs/', include_docs_urls(title='Cine API'))
]

