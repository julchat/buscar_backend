from django.shortcuts import render
from catalogo.models import Catalogo as Catalogo_ORM
from app_mvc.models import Account
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from clases.StorageAdapter import StorageAdapter
from clases.OurLogger import OurLogger
from clases.RNA_Allocator import RNA_Allocator
import time
import shutil
import os
import json
from utils import *
from django.core.files.base import ContentFile
from django.http import JsonResponse

rna_alloc = RNA_Allocator()
sa = StorageAdapter()


def entrenar_rna_view(request, nombre_objeto):
    respuesta = {}
    if request.user.is_authenticated:
        # OBTENEMOS LA INFO DEL MODELO
        account = Account.objects.get(username=request.user.username)
        catalogo = Catalogo_ORM.objects.get(usuario_id=account.id)

        #################
        # NOS OCUPAMOS DEL ENTRENAMIENTO

        logger = OurLogger(request.user.username).get_logger()

        red = rna_alloc.getRNA(account.id)
        status = red.getEstado()

        if status == 'ON_TRAINING':
            #SI SE ESTÁ ENTRENANDO AÚN, NO PODEMOS RE ENTRENARLO
            return HttpResponse("LA RNA ESTÁ EN ENTRENAMIENTO AÚN, POR FAVOR REINTENTE MÁS TARDE")

        configRna = '{"train": "' + nombre_objeto + '"}'
        red.last_obj_on_train = nombre_objeto
        red.setConfig(configRna)
        red.entrenar(catalogo, logger, sa)

        time.sleep(3)

        red.last_obj_on_train = nombre_objeto
        #################

        # IMPRESIÓN RE RESULTADOS
        respuesta = nombre_objeto + "|" + \
                    red.getContainerName() + "|" + red.getEstado() + "|" + red.last_obj_on_train

    return render(request, 'rna/rna_train.html', {
        'respuesta': respuesta
    })

def buscar_rna_view_flutter(request, nombre_objeto):
    respuesta = {}
    if request.method == 'POST' and request.user.is_authenticated:
        fotoSinDeco = request.POST['miArchivo']
        if fotoSinDeco:

            account = Account.objects.get(username=request.user.username)
            path = "temp/" + request.user.username + "/" + nombre_objeto + "/" + nombre_objeto + '.jpeg'
            miArchivoPre = base64_a_imagen(fotoSinDeco)

            # OBTENEMOS LA FOTO DEL RECINTO A ESCANEAR
            miArchivo = ContentFile(miArchivoPre)
            fs = FileSystemStorage()
            foto_recinto = fs.save(path, miArchivo)

            #################
            # NOS OCUPAMOS DE LA BÚSQUEDA
            logger = OurLogger(request.user.username).get_logger()

            ultimo_objeto_on_train = get_ultimo_objeto_on_train(account)

            print(ultimo_objeto_on_train)
            if is_on_training(account) and ultimo_objeto_on_train == nombre_objeto:
                #SI SE ESTÁ ENTRENANDO AÚN, NO PODEMOS BUSCARLO
                return HttpResponse("LA RNA ESTÁ EN ENTRENAMIENTO AÚN PARA ESTE OBJETO, POR FAVOR REINTENTE MÁS TARDE")

            red = rna_alloc.getRNA(account.id)
            configRna = '{"val": "' + nombre_objeto + '"}'
            red.setConfig(configRna)

            try:
                respuesta = red.buscarObjeto(foto_recinto, logger, sa)
            except OSError as e:
                return HttpResponse("LA RNA NO ESTÁ ENTRENADA PARA ESTE OBJETO AÚN.")
            #################

            # LIMPIAMOS LA CARPETA TEMPORAL SIEMPRE Y CUANDO NO HAYA UN TRAININ EN CURSO
            if is_on_training(account):
                os.remove(foto_recinto)
            else:
                shutil.rmtree('temp/' + red.getContainerName() )
            respuesta['encontrado'] = str(respuesta['encontrado'])
            respuesta_json = json.dumps(respuesta)
            diccionario_resultante = json.loads(respuesta_json)
    return JsonResponse(diccionario_resultante, safe=False)

def buscar_rna_view(request, nombre_objeto):
    respuesta = {}
    if request.method == 'POST' and request.FILES['miArchivo'] \
            and request.user.is_authenticated:
        account = Account.objects.get(username=request.user.username)

        # OBTENEMOS LA FOTO DEL RECINTO A ESCANEAR
        miArchivo = request.FILES['miArchivo']
        user_path = "temp/" + request.user.username + "/" + nombre_objeto
        fs = FileSystemStorage(location=user_path)
        foto_recinto = fs.save(miArchivo.name, miArchivo)
        #################
        # NOS OCUPAMOS DE LA BÚSQUEDA
        logger = OurLogger(request.user.username).get_logger()

        red = rna_alloc.getRNA(account.id)

        status = red.getEstado()
        ultimo_objeto_on_train = red.last_obj_on_train

        if status == 'ON_TRAINING' and ultimo_objeto_on_train == nombre_objeto:
            #SI SE ESTÁ ENTRENANDO AÚN, NO PODEMOS BUSCARLO
            return HttpResponse("LA RNA ESTÁ EN ENTRENAMIENTO AÚN PARA ESTE OBJETO, POR FAVOR REINTENTE MÁS TARDE")

        configRna = '{"val": "' + nombre_objeto + '"}'
        red.setConfig(configRna)

        foto_recinto = user_path + "/" + foto_recinto

        try:
            respuesta = red.buscarObjeto(foto_recinto, logger, sa)
        except OSError as e:
            return HttpResponse("LA RNA NO ESTÁ ENTRENADA PARA ESTE OBJETO AÚN.")
        #################

        # LIMPIAMOS LA CARPETA TEMPORAL SIEMPRE Y CUANDO NO HAYA UN TRAININ EN CURSO
        if status == 'ON_TRAINING':
            os.remove(foto_recinto)
        else:
            shutil.rmtree('temp/' + red.getContainerName() )
    return render(request, 'rna/rna_test.html', respuesta)


def get_estado_rna_view(request):
    status = "DESCONOCIDO"
    if request.user.is_authenticated:
        # OBTENEMOS LA INFO DEL MODELO
        account = Account.objects.get(username=request.user.username)
        red = rna_alloc.getRNA(account.id)
        status = red.getEstado()

    return HttpResponse(status)