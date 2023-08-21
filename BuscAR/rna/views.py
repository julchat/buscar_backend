from django.shortcuts import render
from rna.models import RNA as RNA_ORM
from catalogo.models import Catalogo as Catalogo_ORM
from catalogo.models import Objeto as Objeto_ORM
from app_mvc.models import Account
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from clases.StorageAdapter import StorageAdapter
from clases.OurLogger import OurLogger
from clases.RNA_Allocator import RNA_Allocator
import time
import shutil


rna_alloc = RNA_Allocator()
sa = StorageAdapter()


def entrenar_rna_view(request, nombre_objeto):
    respuesta = {}
    if request.user.is_authenticated:
        # OBTENEMOS LA INFO DEL MODELO
        account = Account.objects.get(username=request.user.username)
        catalogo = Catalogo_ORM.objects.get(usuario_id=account.id)

        logger = OurLogger(request.user.username).get_logger()

        # IMPLEMENTAR ACÁ EL RNA ALLOCATOR
        #################
        red = RNA_ORM.objects.get(user_id=account.id)
        configRna = '{"train": "' + nombre_objeto + '"}'
        red.setConfig(configRna)
        red.entrenar(catalogo, logger, sa)

        time.sleep(3)

        print(red.last_obj_on_train)
        red.last_obj_on_train = nombre_objeto
        print(red.getEstado())
        #################

        # LINEA DE PRUEBA
        respuesta = nombre_objeto + " - " + \
                    red.getContainerName() + " - " + red.getEstado() + " - " + red.last_obj_on_train

    return render(request, 'rna/rna_train.html', {
        'respuesta': respuesta
    })


def buscar_rna_view(request, nombre_objeto):
    respuesta = {}
    if request.method == 'POST' and request.FILES['miArchivo'] \
            and request.user.is_authenticated:
        account = Account.objects.get(username=request.user.username)

        # OBTENEMOS LA FOTO DEL RECINTO A ESCANEAR
        miArchivo = request.FILES['miArchivo']
        # objeto = request.POST['objNombre']

        user_path = "temp/" + request.user.username + "/" + nombre_objeto
        fs = FileSystemStorage(location=user_path)
        foto_recinto = fs.save(miArchivo.name, miArchivo)

        # IMPLEMENTAR ACÁ EL RNA ALLOCATOR
        #################
        logger = OurLogger(request.user.username).get_logger()
        red = RNA_ORM.objects.get(user_id=account.id)
        configRna = '{"val": "' + nombre_objeto + '"}'
        red.setConfig(configRna)

        foto_recinto = user_path + "/" + foto_recinto
        print(foto_recinto)
        respuesta = red.buscarObjeto(foto_recinto, logger, sa)
        #################

        # LINEA DE PRUEBA
        print(respuesta)
        shutil.rmtree('temp/' + red.getContainerName() )

    return render(request, 'rna/rna_test.html', respuesta)
