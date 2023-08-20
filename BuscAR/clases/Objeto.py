class Objeto:
    def __init__(self, nombre):
        self.nombre = nombre
        self.fotosUrl = []
        self.xmlUrl = []

    def agregarArchivo(self, file):
        if file[-4:] == '.xml':
            self.xmlUrl.append(file)
        elif file[-4:] in ['.jpg', 'jpeg', '.png']:
            self.fotosUrl.append(file)

    def getFotos(self):
        return self.fotosUrl

    def getXml(self):
        return self.xmlUrl