from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from catalogo.models import *
from app_mvc.models import Account
from clases.StorageAdapter import *

sa = StorageAdapter()


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
