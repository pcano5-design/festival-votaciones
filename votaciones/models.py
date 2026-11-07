from django.core.exceptions import ValidationError
from django.db import models


class Edicion(models.Model):
    nombre = models.CharField(max_length=150)
    anio = models.PositiveIntegerField('año', unique=True)
    fecha_inicio = models.DateField('fecha de inicio')
    fecha_fin = models.DateField('fecha de fin')
    activa = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'edición'
        verbose_name_plural = 'ediciones'
        ordering = ['-anio']

    def __str__(self):
        return f'{self.nombre} ({self.anio})'

    def clean(self):
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio.')
        

class Categoria(models.Model):
    edicion = models.ForeignKey(
        Edicion,
        on_delete=models.PROTECT,
        related_name='categorias',
        verbose_name='edición',
    )
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField('descripción', blank=True)

    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'
        ordering = ['edicion', 'nombre']
        constraints = [
            models.UniqueConstraint(
                fields=['edicion', 'nombre'],
                name='categoria_unica_por_edicion',
            ),
        ]

    def __str__(self):
        return f'{self.nombre} - {self.edicion.anio}'
    

class Votacion(models.Model):
    ESTADOS = [
        ('borrador', 'Borrador'),
        ('abierta', 'Abierta'),
        ('cerrada', 'Cerrada'),
    ]

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='votaciones',
        verbose_name='categoría',
    )
    titulo = models.CharField('título', max_length=200)
    descripcion = models.TextField('descripción', blank=True)
    fecha_apertura = models.DateTimeField('fecha de apertura')
    fecha_cierre = models.DateTimeField('fecha de cierre')
    estado = models.CharField(max_length=10, choices=ESTADOS, default='borrador')

    class Meta:
        verbose_name = 'votación'
        verbose_name_plural = 'votaciones'
        ordering = ['fecha_apertura']

    def __str__(self):
        return self.titulo

    def clean(self):
        if self.fecha_apertura and self.fecha_cierre and self.fecha_cierre <= self.fecha_apertura:
            raise ValidationError('La fecha de cierre debe ser posterior a la fecha de apertura.')
        

class Opcion(models.Model):
    votacion = models.ForeignKey(
        Votacion,
        on_delete=models.CASCADE,
        related_name='opciones',
        verbose_name='votación',
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField('descripción', blank=True)
    orden = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'opción'
        verbose_name_plural = 'opciones'
        ordering = ['votacion', 'orden']
        constraints = [
            models.UniqueConstraint(
                fields=['votacion', 'nombre'],
                name='opcion_unica_por_votacion',
            ),
        ]

    def __str__(self):
        return self.nombre