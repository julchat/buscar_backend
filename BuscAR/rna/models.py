from django.db import models
from django.conf import settings
import threading
import json
from clases.KernelRna import KernelRna


class RNA(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, related_name="user_rna")
    containerName = models.CharField(max_length=250)
    # configRna = models.CharField(max_length=250)
    configRna = ""
    rna_train = None
    rna_val = None
    last_obj_on_train = ""

    def __str__(self):
        return self.containerName

    def getContainerName(self):
        return self.containerName

    def getEstado(self):
        if self.rna_train is None:
            return 'No hay red de train seteada'
        else:
            if self.rna_train.getStatus() == 0:
                return 'READY'
            else:
                return 'ON_TRAINING'

    def setConfig(self, configRna):
        json_config = json.loads(configRna)

        res = self.getEstado()
        if res == 'ON_TRAINING':
            if 'train' in json_config:
                return 'Aún se está entrenando otro objeto'
        else:
            if 'train' in json_config:
                t = json_config['train']
                self.rna_train = KernelRna(self.containerName, t)

        if 'val' in json_config:
            v = json_config['val']
            self.rna_val = KernelRna(self.containerName, v)

        else:
            self.rna_val = None

    def entrenar(self, catalogo, logger, singleton):
        if self.rna_train is None:
            logger.error('No se ha seteado algo para entrenar en la configRna')
        else:
            hilo1 = threading.Thread(target=self.rna_train.entrenar, args=(catalogo, logger, singleton))
            hilo1.start()

    def buscarObjeto(self, recinto, logger, singleton):
        if self.rna_val is None:
            logger.error('No se a seteado algo para validar en la configRna')
        else:
            result = self.rna_val.buscarObjeto(recinto, logger, singleton)
            return result
