

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
        # guardarArchivo(url, file): void
        pass

    def obtenerArchivo(self, url):
        # obtenerArchivo(url): file
        pass

    def borrarArchivo(self, url):
        # borrarArchivo(url): file
        pass
