from django.urls import path

from . import views

app_name = 'votaciones'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('edicion/<int:anio>/', views.detalle_edicion, name='detalle_edicion'),
    path('votacion/<int:pk>/', views.detalle_votacion, name='detalle_votacion'),
]