from rna.models import RNA as RNA_ORM


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

    def getRNA(self, user_id):
        for red in self.rnas:
            if red.user_id == user_id:
                # SI encuentra una RNA, la devuelve
                return red
        # SI NO HAY RNA CREADA, OBTENEMOS UNA INSTANCIA Y LA DEVOLVEMOS
        result = RNA_ORM.objects.get(user_id=user_id)
        self.rnas.append(result)

        return result

