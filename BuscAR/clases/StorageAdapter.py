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

    def _obtenerEquivalenteEnStorage(self, path):
        url_t = 'storage/'
        url = path.replace('\\', '/')
        l = url.split('/')
        l = l[1:]
        for t in l:
            url_t += t + '/'
        url_t = url_t[:-1]

        return url_t

    def _obtenerUsuario(self, path):
        url = path.replace('\\', '/')
        l = url.split('/')
        return l[1]

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
        shutil.copytree(url, url_t, dirs_exist_ok=True)

        user = self._obtenerUsuario(url)
        shutil.rmtree('temp/' + user)

    def guardarArchivo(self, url, file):
        # TOMA LOS ARHIVOS DE LA CARPETA TEMPORAL Y LOS MUEVE al STORAGE
        url_t = self._obtenerEquivalenteEnStorage(url)
        url_t += self.obtenerCarpetaParaObjeto(file)

        self.crearDirectorio(url_t)
        shutil.copy(url + file , url_t + file)

        user = self._obtenerUsuario(url)
        shutil.rmtree('temp/' + user)
        # guardarArchivo(url, file): void

    def obtenerArchivo(self, url):
        # obtenerArchivo(url): file
        return "storage/" + url

    def obtenerDirectorio(self, url):
        # obtenerDirectorio(url): file
        return "storage/" + url

    def borrarDirectorio(self, url):
        shutil.rmtree('storage/' + url)

