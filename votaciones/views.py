from django.shortcuts import get_object_or_404, render

from .models import Edicion, Votacion


def inicio(request):
    ediciones = Edicion.objects.all()
    return render(request, 'votaciones/inicio.html', {'ediciones': ediciones})


def detalle_edicion(request, anio):
    edicion = get_object_or_404(Edicion, anio=anio)
    categorias = edicion.categorias.all()
    votaciones = (
        Votacion.objects
        .filter(categoria__edicion=edicion)
        .exclude(estado='borrador')
    )
    return render(request, 'votaciones/detalle_edicion.html', {
        'edicion': edicion,
        'categorias': categorias,
        'votaciones': votaciones,
    })


def detalle_votacion(request, pk):
    votacion = get_object_or_404(
        Votacion.objects.exclude(estado='borrador'),
        pk=pk,
    )
    opciones = votacion.opciones.all()
    return render(request, 'votaciones/detalle_votacion.html', {
        'votacion': votacion,
        'opciones': opciones,
    })