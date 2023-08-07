from django.shortcuts import render
from rna.models import *
from catalogo.models import *
from app_mvc.models import Account
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage


def entrenar_rna_view(request):
    respuesta = {}
    if request.user.is_authenticated:
        account = Account.objects.get(username=request.user.username)
        red = RNA.objects.get(user_id=account.id)
        catalogo = Catalogo.objects.get(usuario_id=account.id)

        respuesta = red.entrenar(catalogo)

    return render(request, 'rna/rna_train.html', {
            'respuesta': respuesta
        })


def buscar_rna_view(request):
    respuesta = {}
    if request.method == 'POST' and request.FILES['miArchivo'] \
            and request.user.is_authenticated:
        account = Account.objects.get(username=request.user.username)
        catalogo = Catalogo.objects.get(usuario_id=account.id)
        red = RNA.objects.get(user_id=account.id)

        miArchivo = request.FILES['miArchivo']
        objeto = request.POST['objNombre']

        user_path = "temp/" + request.user.username + "/" + objeto
        fs = FileSystemStorage(location=user_path)
        foto_recinto = fs.save(miArchivo.name, miArchivo)
        try:
            objeto_db = Objeto.objects.get(catalogo_id=catalogo.id, nombre=objeto)
        except:
            return HttpResponse("EL OBJETO NO EXISTE EN EL CATALOGO DEL USUARIO DADO")

        respuesta = red.buscarObjeto(foto_recinto, objeto_db)
        print(respuesta)

    return render(request, 'rna/rna_test.html', respuesta)