from django.db import models
from django.conf import settings


class Catalogo(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, related_name="user_catalog")
    containerName = models.CharField(max_length=250)

    def __str__(self):
        return self.containerName

    def getObjeto(self, nombre):
        objeto = Objeto.objects.get(catalogo_id=self.id, nombre=nombre)
        return objeto

    def agregarObjeto(self, obj):
        pass


class Objeto(models.Model):
    catalogo = models.ForeignKey(Catalogo,
                                 on_delete=models.CASCADE, related_name="catalogo")
    nombre = models.CharField(max_length=250)

    def __str__(self):
        return self.nombre

    def getArchivos(self):
        catalogo = Catalogo.objects.get(id=self.catalogo_id)
        filenames_db = FotoUrl.objects.filter(objeto_id=self.id)
        paths = []
        for f in filenames_db:
            path = "storage/" + catalogo.containerName + "/" + self.nombre + "/" + f.textoUrl
            paths.append(path)
        return paths

    def esXml(self, file):
        if file[-4:] == '.xml':
            return True
        return False

    def esFoto(self, file):
        if file[-4:] in ['.jpg', 'jpeg', '.png']:
            return True
        return False

    def getFotos(self):
        url_varias = self.getArchivos()
        fotos = filter(self.esFoto, url_varias)
        return list(fotos)

    def getXml(self):
        url_varias = self.getArchivos()
        xmls = filter(self.esXml, url_varias)
        return list(xmls)


class FotoUrl(models.Model):
    objeto = models.ForeignKey(Objeto,
                                 on_delete=models.CASCADE, related_name="objeto")
    textoUrl = models.CharField(max_length=250)

    # orden = models.IntegerField()

    def __str__(self):
        return self.textoUrl
