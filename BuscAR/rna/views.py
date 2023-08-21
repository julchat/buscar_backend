from django.shortcuts import render
from rna.models import RNA as RNA_ORM
from catalogo.models import Catalogo as Catalogo_ORM
from catalogo.models import Objeto as Objeto_ORM
from catalogo.models import FotoUrl as FotoUrl_ORM
from app_mvc.models import Account
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from clases.StorageAdapter import StorageAdapter
from clases.OurLogger import OurLogger
from clases.RNA_Allocator import RNA_Allocator

rna_alloc = RNA_Allocator()


def entrenar_rna_view(request, nombre_objeto):
    respuesta = {}
    if request.user.is_authenticated:
        # OBTENEMOS LA INFO DEL MODELO
        account = Account.objects.get(username=request.user.username)
        red = RNA_ORM.objects.get(user_id=account.id)
        catalogo = Catalogo_ORM.objects.get(usuario_id=account.id)

        objeto = catalogo.getObjeto(nombre_objeto)

        # GENERAMOS EL MODELO TEMPORAL PARA QUE NO SE SUPERPONGA CON OTROS OBJETOS Y SEA USADO POR LA RNA

        # CONTINUAR ACÁ, CON LAS VALIDACIONES DE SI está entrenando o no

        respuesta = red.entrenar(catalogo) + " - " + nombre_objeto

    return render(request, 'rna/rna_train.html', {
        'respuesta': respuesta,
        'paths': paths
    })


def buscar_rna_view(request, nombre_objeto):
    respuesta = {}
    if request.method == 'POST' and request.FILES['miArchivo'] \
            and request.user.is_authenticated:
        account = Account.objects.get(username=request.user.username)
        catalogo = Catalogo_ORM.objects.get(usuario_id=account.id)
        red = RNA_ORM.objects.get(user_id=account.id)

        miArchivo = request.FILES['miArchivo']
        objeto = request.POST['objNombre']

        user_path = "temp/" + request.user.username + "/" + objeto
        fs = FileSystemStorage(location=user_path)
        foto_recinto = fs.save(miArchivo.name, miArchivo)
        try:
            objeto_db = Objeto_ORM.objects.get(catalogo_id=catalogo.id, nombre=objeto)
        except:
            return HttpResponse("EL OBJETO NO EXISTE EN EL CATALOGO DEL USUARIO DADO")

        respuesta = red.buscarObjeto(foto_recinto, objeto_db)
        print(respuesta)

    return render(request, 'rna/rna_test.html', respuesta)
