import os


class StorageAdapter(object):
    # MÉTODOS DE CLASE // IMPLEMENTACIÓN DEL SINGLETON
    _instancias = None

    def __new__(cls):
        if cls._instancias is None:
            obj = super().__new__(cls)
            cls._instancias = obj
        return cls._instancias

    # METODOS DE ISNTANCIA
    def __init__(self):
        self.cuantaUrl = "url_account_stoagre"   # cambiar según el deployment de Azure

    def guardarArchivo(self, url, file):
        # SI 'file' == '', entonces se crea el directorio en 'url'

        if file == '':
            if not os.path.exists(url):
                os.makedirs(url)
        # guardarArchivo(url, file): void

    def obtenerArchivo(self, url):
        # obtenerArchivo(url): file
        pass

    def borrarArchivo(self, url):
        # borrarArchivo(url): file
        pass
