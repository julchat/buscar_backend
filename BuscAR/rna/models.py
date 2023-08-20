from django.db import models
from django.conf import settings
from clases.OurLogger import OurLogger


class RNA(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, related_name="user_rna")
    containerName = models.CharField(max_length=250)
    # configRna = models.CharField(max_length=250)
    configRna = ""

    def __str__(self):
        return self.containerName

    def entrenar(self, catalogo):
        # entrenar(catalogo): void
        print("ENTRENAMIENTO")
        return "ENTRENAMIENTO"

    def buscarObjeto(self, recinto, objeto):
        # buscarObjeto(recinto, objeto): Dictionary
        print("MODO BÚSQUEDA")
        return {'encontrado' : 'sabe Dios'}
