from django.db import models
from django.conf import settings


class Catalogo(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, related_name="user_catalog")
    containerName = models.CharField(max_length=250)

    def __str__(self):
        return self.containerName


class Objeto(models.Model):
    catalogo = models.ForeignKey(Catalogo,
                                 on_delete=models.CASCADE, related_name="catalogo")
    nombre = models.CharField(max_length=250)
    fotosUrl = []

    def __str__(self):
        return self.nombre


class fotoUrl(models.Model):
    objeto = models.ForeignKey(Objeto,
                                 on_delete=models.CASCADE, related_name="objeto")
    textoUrl = models.CharField(max_length=250)

    # orden = models.IntegerField()

    def __str__(self):
        return self.textoUrl
