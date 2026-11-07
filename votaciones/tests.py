from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Categoria, Edicion, Opcion, Votacion


class VotacionesTests(TestCase):

    def setUp(self):
        self.edicion = Edicion.objects.create(
            nombre='Edición de prueba', anio=2027,
            fecha_inicio=date(2027, 4, 28), fecha_fin=date(2027, 5, 1), activa=True,
        )
        self.categoria = Categoria.objects.create(edicion=self.edicion, nombre='Piquería')
        ahora = timezone.now()
        self.abierta = Votacion.objects.create(
            categoria=self.categoria, titulo='Votación abierta',
            fecha_apertura=ahora, fecha_cierre=ahora + timedelta(days=1), estado='abierta',
        )
        self.borrador = Votacion.objects.create(
            categoria=self.categoria, titulo='Votación en borrador',
            fecha_apertura=ahora, fecha_cierre=ahora + timedelta(days=1), estado='borrador',
        )
        Opcion.objects.create(votacion=self.abierta, nombre='Opción A', orden=1)

    def test_inicio_muestra_ediciones(self):
        respuesta = self.client.get(reverse('votaciones:inicio'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Edición de prueba')

    def test_borrador_no_aparece_al_publico(self):
        respuesta = self.client.get(reverse('votaciones:detalle_edicion', args=[2027]))
        self.assertContains(respuesta, 'Votación abierta')
        self.assertNotContains(respuesta, 'Votación en borrador')

    def test_borrador_da_404_por_url(self):
        respuesta = self.client.get(reverse('votaciones:detalle_votacion', args=[self.borrador.pk]))
        self.assertEqual(respuesta.status_code, 404)

    def test_fechas_invalidas_en_edicion(self):
        edicion = Edicion(
            nombre='Edición mala', anio=2030,
            fecha_inicio=date(2030, 5, 1), fecha_fin=date(2030, 4, 1),
        )
        with self.assertRaises(ValidationError):
            edicion.full_clean()