class RNA_Allocator(object):
    # MÉTODOS DE CLASE // IMPLEMENTACIÓN DEL SINGLETON
    _instancias = None

    def __new__(cls):
        if cls._instancias is None:
            obj = super().__new__(cls)
            cls._instancias = obj
        return cls._instancias

    # METODOS DE INSTANCIA
    def __init__(self):
        self.rnas = []

    def getRNA(self, name):
        for red in self.rnas:
            if red.getContainerName() == name:
                return red
        result = None # INSTANCIAR LA DE GIAN Y DEVOLVERLA
        return result
