from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from app_mvc.forms import RegistrationForm, AccountAuthenticationForm
from django.middleware.csrf import get_token
from django.http import JsonResponse

def csrf_token_view(request):
    csrf_token = get_token(request)
    return HttpResponse(csrf_token)

def home_view(request):
    context = {}
    return render(request, "app_mvc/home.html", context)


def register_view(request, *args, **kwargs):
    print(request)
    print(request.user)
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"Ya has ingresado como {user.email}")
    context = {}

    if request.POST:
        print (request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print (request.POST)
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect("home")
        else:
            form = RegistrationForm()
            context['registration_form'] = form

    return render(request, 'app_mvc/register.html', context)

def register_view_flutter(request, *args, **kwargs):
    print(request)
    print(request.user)
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"Ya has ingresado como {user.email}")
    context = {}

    if request.POST:
        print (request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print (request.POST)
            form.save()
            return JsonResponse({'message': 'Exitoso'}, status=200)
        else:
            form = RegistrationForm()
            context['registration_form'] = form
            return JsonResponse({'message': 'Fallido'}, status=400)

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

def login_view_flutter(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        print('Ya has ingresado como user')
        return redirect("home")

    if request.POST:
        print(request.POST)
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                print('logeado')
                return redirect("home")
        else:
            context['login_form'] = form
    return render(request, "app_mvc/login.html", context)

def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect
