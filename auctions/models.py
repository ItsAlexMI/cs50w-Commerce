from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    pass

class Listado(models.Model):
    
    titulo = models.CharField(max_length=200, help_text="Título del listado")
    descripcion = models.TextField(help_text="Descripción del listado")
    oferta_inicial = models.DecimalField(max_digits=10, decimal_places=2, help_text="Oferta inicial")


    url_imagen = models.URLField(blank=True, null=True, help_text="URL de la imagen del listado")
    categoria = models.CharField(max_length=100, blank=True, null=True, help_text="Categoría del listado")

    abierto = models.BooleanField(default=True, help_text="¿El listado está abierto?")

    autorListado = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listados", null=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    subasta_cerrada = models.BooleanField(default=False)
    
    def __str__(self):
        return self.titulo

class ListaSeguimiento (models.Model):
    listado = models.ForeignKey(Listado, on_delete=models.CASCADE, related_name="seguidores")
    seguidor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Seguimiento de {self.seguidor.username} en {self.listado.titulo}"


class Oferta(models.Model):
    listado = models.ForeignKey(Listado, on_delete=models.CASCADE, related_name="ofertas", null=True)
    postor = models.ForeignKey(User, on_delete=models.CASCADE)
    monto_oferta = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Oferta de {self.postor.username} en {self.listado.titulo}"

class Comentario(models.Model):
    listado = models.ForeignKey(Listado, on_delete=models.CASCADE, related_name="comentarios")
    comentarista = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.comentarista.username} en {self.listado.titulo}"
    
