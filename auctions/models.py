from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listado(models.Model):
    titulo = models.CharField(max_length=200, help_text="Título del listado")
    descripcion = models.TextField(help_text="Descripción del listado")
    oferta_inicial = models.DecimalField(max_digits=10, decimal_places=2, help_text="Oferta inicial")

    url_imagen = models.URLField(blank=True, null=True, help_text="URL de la imagen del listado")
    categoria = models.CharField(max_length=100, blank=True, null=True, help_text="Categoría del listado")

    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Subasta(models.Model):
    listado = models.ForeignKey(Listado, on_delete=models.CASCADE, related_name="subastas")
    hora_inicio = models.DateTimeField()
    hora_fin = models.DateTimeField()
    oferta_actual = models.DecimalField(max_digits=10, decimal_places=2)
    ganador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Subasta de {self.listado.titulo}"

class Oferta(models.Model):
    subasta = models.ForeignKey(Subasta, on_delete=models.CASCADE, related_name="ofertas")
    postor = models.ForeignKey(User, on_delete=models.CASCADE)
    monto_oferta = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Oferta de {self.postor.username} en {self.subasta.listado.titulo}"

class Comentario(models.Model):
    listado = models.ForeignKey(Listado, on_delete=models.CASCADE, related_name="comentarios")
    comentarista = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.comentarista.username} en {self.listado.titulo}"