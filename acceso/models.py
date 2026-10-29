import uuid
from django.db import models

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    curso = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} ({self.curso})"

class Apoderado(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=15)
    autorizado = models.BooleanField(default=True)
    token_qr = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    foto = models.ImageField(upload_to='apoderados/', null=True, blank=True)
    alumnos = models.ManyToManyField(Alumno, related_name='apoderados')

    def __str__(self):
        estado = "AUTORIZADO" if self.autorizado else "NO AUTORIZADO"
        return f"{self.nombre} - {estado}"

class RegistroAcceso(models.Model):
    apoderado = models.ForeignKey(Apoderado, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    permitido = models.BooleanField()

    def __str__(self):
        return f"{self.apoderado.nombre} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}"
