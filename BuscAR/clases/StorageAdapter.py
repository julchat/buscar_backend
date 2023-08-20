import os
import shutil


class StorageAdapter(object):
    # MÉTODOS DE CLASE // IMPLEMENTACIÓN DEL SINGLETON
    _instancias = None

    def __new__(cls):
        if cls._instancias is None:
            obj = super().__new__(cls)
            cls._instancias = obj
        return cls._instancias

    # METODOS DE INSTANCIA
    def __init__(self):
        self.cuantaUrl = "url_account_stoagre"   # cambiar según el deployment de Azure

    def _obtenerEquivalenteEnStorage(self, url):
        url_t = 'storage/'
        l = url.split('/')
        l = l[1:]
        for t in l:
            url_t += t + '/'
        url_t = url_t[:-1]

        return url_t

    def obtenerCarpetaParaObjeto(self,file):
        url_t = ''
        if file[-4:] == '.xml':
            url_t = 'xml/'
        elif file[-4:] in ['.jpg', 'jpeg', '.png']:
            url_t = 'train/'
        else:
            url_t = 'otros/'
        return url_t

    def crearDirectorio(self, url):
        # CREA UN DIRECTORIO, SI NO EXISTE
        if not os.path.exists(url):
            os.makedirs(url)

    def guardarDirectorio(self, url):
        # TOMA LOS ARHIVOS DE LA CARPETA TEMPORAL Y LOS MUEVE al storage
        url_t = self._obtenerEquivalenteEnStorage(url)
        shutil.copytree(url, url_t)
        shutil.rmtree('temp/')

    def guardarArchivo(self, url, file):
        # TOMA LOS ARHIVOS DE LA CARPETA TEMPORAL Y LOS MUEVE al STORAGE
        url_t = self._obtenerEquivalenteEnStorage(url)
        url_t += self.obtenerCarpetaParaObjeto(file)

        self.crearDirectorio(url_t)
        shutil.copy(url + file , url_t + file)
        shutil.rmtree('temp/')
        # guardarArchivo(url, file): void

    def obtenerArchivo(self, url):
        # obtenerArchivo(url): file
        return url

    def borrarArchivo(self, url):
        # borrarArchivo(url): file
        pass
