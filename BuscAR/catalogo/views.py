from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from catalogo.models import *
from app_mvc.models import Account
from clases.StorageAdapter import *
from utils import *
from django.http import JsonResponse
from django.core.files.base import ContentFile

sa = StorageAdapter()

def mostrar_objetos_flutter(request):
    objetos = []
    if request.user.is_authenticated:
        account = Account.objects.get(username=request.user.username)
        catalogo = Catalogo.objects.get(usuario_id=account.id)
        objetos = Objeto.objects.filter(catalogo_id=catalogo.id)

        objetos_listos = []
        for o in objetos:
            olisto = {}
            olisto['id'] = o.id
            fotos = o.getFotos()
            olisto['primerafoto'] = imagen_a_base64(fotos[0])
            olisto['nombre'] = o.nombre

            if get_ultimo_objeto_on_train(account) == o.nombre and is_on_training(account):
                olisto['detectable'] = False
            else:
                olisto['detectable'] = True
            objetos_listos.append(olisto)
        
        esta_vacio = False if objetos_listos else True
        if esta_vacio:
            return JsonResponse({'vacio' : esta_vacio, 'objetos' : ''}, status = 200)
        else:
            return JsonResponse({'vacio' : esta_vacio, 'objetos' : objetos_listos}, status = 200)

def mostrar_objetos(request):
    objetos = []
    if request.user.is_authenticated:
        account = Account.objects.get(username=request.user.username)
        catalogo = Catalogo.objects.get(usuario_id=account.id)
        objetos = Objeto.objects.filter(catalogo_id=catalogo.id)

        #MOSTRAMOS DE PASO LAS FOTOS
        paths = []
        for o in objetos:
            paths += o.getFotos()
            paths += o.getXml()

    return render(request, 'catalogo/mostrar_obj.html', {
        'objetos': objetos ,
        'paths' : paths
    })

def crear_actualizar_objeto_view_flutter(request):
    if request.method == 'POST' and request.POST['miArchivo'] \
    and request.user.is_authenticated:
        fotoSinDeco = request.POST['miArchivo']
        objeto = request.POST['objNombre']
        nombre = request.POST['archivoNombre']
        user_path = "temp/" + request.user.username + "/" + objeto + "/"

        miArchivoPre = base64_a_imagen(fotoSinDeco)
        miArchivo = ContentFile(miArchivoPre)

        fs = FileSystemStorage(location=user_path)
        filename = fs.save(nombre, miArchivo)

        # USAR ESTO CUANDO SE HABILITE EL STORAGEADAPTER DE AZURE
        sa.guardarArchivo(user_path, filename)

        uploaded_file_url = fs.url(filename)

        # PERSISTIMOS EL NUEVO OBJETO MÁS ALLA DE LAS IMAGENES
        account = Account.objects.get(username=request.user.username)
        catalogo = Catalogo.objects.get(usuario_id=account.id)

        # SI NO EXISTE EL OBJETO, LO CREAMOS
        try:
            objeto_db = Objeto.objects.get(catalogo_id=catalogo.id, nombre=objeto)
        except:
            objeto_db = Objeto(catalogo = catalogo, nombre=objeto)
            objeto_db.save()

        url_archivo = sa.obtenerCarpetaParaObjeto(filename) + filename
        archivo_asoc = FotoUrl(objeto=objeto_db, textoUrl=url_archivo)
        archivo_asoc.save()

        return JsonResponse({'resultado' : 'exito', 'descripcion' : 'foto agregada con exito'}, status = 200)
    return JsonResponse({'resultado' : 'error', 'descripcion' : 'fallo la autenticacion'}, status = 400)

def crear_actualizar_objeto_view(request):
    if request.method == 'POST' and request.FILES['miArchivo'] \
            and request.user.is_authenticated:
        miArchivo = request.FILES['miArchivo']
        objeto = request.POST['objNombre']
        user_path = "temp/" + request.user.username + "/" + objeto + "/"
        fs = FileSystemStorage(location=user_path)
        filename = fs.save(miArchivo.name, miArchivo)

        # USAR ESTO CUANDO SE HABILITE EL STORAGEADAPTER DE AZURE
        sa.guardarArchivo(user_path, filename)

        uploaded_file_url = fs.url(filename)

        # PERSISTIMOS EL NUEVO OBJETO MÁS ALLA DE LAS IMAGENES
        account = Account.objects.get(username=request.user.username)
        catalogo = Catalogo.objects.get(usuario_id=account.id)

        # SI NO EXISTE EL OBJETO, LO CREAMOS
        try:
            objeto_db = Objeto.objects.get(catalogo_id=catalogo.id, nombre=objeto)
        except:
            objeto_db = Objeto(catalogo = catalogo, nombre=objeto)
            objeto_db.save()

        url_archivo = sa.obtenerCarpetaParaObjeto(filename) + filename
        archivo_asoc = FotoUrl(objeto=objeto_db, textoUrl=url_archivo)
        archivo_asoc.save()

        return render(request, 'catalogo/upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'catalogo/upload.html')
