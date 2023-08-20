class Catalogo:
    def __init__(self, containerName):
        self.containerName = containerName
        self.objetos = []

    def agregarObjeto(self, obj):
        self.objetos.append(obj)

    def getObjeto(self,name):
        for o in self.objetos:
            if o.nombre == name:
                return o