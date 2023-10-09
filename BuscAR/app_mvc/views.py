from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from app_mvc.forms import RegistrationForm, AccountAuthenticationForm
from django.middleware.csrf import get_token
from django.http import JsonResponse
from rna.models import *
from catalogo.models import *
from clases.StorageAdapter import *

sa = StorageAdapter()


def csrf_token_view(request):
    csrf_token = get_token(request)
    return HttpResponse(csrf_token)


def home_view(request):
    context = {}
    return render(request, "app_mvc/home.html", context)


def register_flutter_view(request, *args, **kwargs):
    print(request)
    print(request.user)
    context = {}

    if request.POST:
        print(request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print(request.POST)
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)

            accesorias_alta_de_usuario(account)
            
            return JsonResponse({'message': 'Exitoso'}, status=200)
        else:
            form = RegistrationForm()
            context['registration_form'] = form
            return JsonResponse({'message': 'Fallido'}, status=400)


def logout_flutter_view(request):
    logout(request)
    return JsonResponse({'logoutstatus': 'OK'}, status=200)


def login_flutter_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        print('Ya has ingresado como user')
        return redirect("home")

    if request.POST:
        print(request.POST)
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            print('formvalido')
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                print('logeado')
                print(request.user)
                token = get_token(request)
                print(request.session.session_key)
                session_key = request.session.session_key
                return JsonResponse({'usuario': user.username, 'token': token, 'session': session_key}, status=200)
        else:
            print('Form no valido')
            context['login_form'] = form
        return JsonResponse({'usuario': 'HUBO UN ERROR EN LAS CREDENCIALES'}, status=400)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect


#####################################################################################
######################### COMENTAR CUANDO SE PASE A FLUTTER #########################
#####################################################################################

def logout_view(request):
    logout(request)
    return redirect("home")


def login_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect("home")
        else:
            context['login_form'] = form
    return render(request, "app_mvc/login.html", context)


def register_view(request, *args, **kwargs):
    # print(request)
    # print(request.user)
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"Ya has ingresado como {user.email}")
    context = {}

    if request.POST:
        # print(request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # print(request.POST)
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)

            accesorias_alta_de_usuario(account)

            login(request, account)

            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect("home")
        else:
            form = RegistrationForm()
            context['registration_form'] = form

    return render(request, 'app_mvc/register.html', context)


def accesorias_alta_de_usuario(user):
    if user.is_authenticated:
        containerName = user.username
        path_cat_fotos_inicial = "storage/" + containerName
        sa.crearDirectorio(path_cat_fotos_inicial)

        catalogo = Catalogo(usuario=user, containerName=containerName)
        catalogo.save()

        red = RNA(user=user, containerName=containerName)
        red.save()
