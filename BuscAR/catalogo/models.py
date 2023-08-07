from django.db import models
from django.conf import settings
from clases.OurLogger import OurLogger
from clases.StorageAdapter import StorageAdapter


class Catalogo(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, related_name="user_catalog")
    containerName = models.CharField(max_length=250)

    def __str__(self):
        return self.containerName

    def agregarObjeto(self, nombre, lista_fotos):
        # agregarObjeto(nombre, [foto]): void
        pass

    def removerObjeto(self, nombre):
        # removerObjeto(nombre): void
        pass

    def getObjeto(self, nombre):
        # getObjeto(String): Objeto
        pass

    def getLocacionUrl(self):
        # getLocacionUrl(): String
        pass


class Objeto(models.Model):
    catalogo = models.ForeignKey(Catalogo,
                                 on_delete=models.CASCADE, related_name="catalogo")
    nombre = models.CharField(max_length=250)
    fotosUrl = []

    def __str__(self):
        return self.nombre

    def getFotos(self):
        # getFotos(): List[imagen]
        pass

    def agregarFoto(self, imagen):
        # agregarFoto(imagen): void
        pass


class FotoUrl(models.Model):
    objeto = models.ForeignKey(Objeto,
                                 on_delete=models.CASCADE, related_name="objeto")
    textoUrl = models.CharField(max_length=250)

    # orden = models.IntegerField()

    def __str__(self):
        return self.textoUrl
