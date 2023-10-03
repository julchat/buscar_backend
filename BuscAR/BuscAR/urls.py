"""
URL configuration for BuscAR project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app_mvc import views as user_views
from catalogo import views as catalog_views
from rna import views as rna_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home_view, name="home"),
    path('register_flutter/', user_views.register_flutter_view, name="register_flutter"),
    path('login_flutter/', user_views.login_flutter_view, name="login_flutter"),
    path('logout_flutter/', user_views.logout_flutter_view, name='logout_flutter'),

    # VULNERABLE - ELIMINAR / COMENTAR CUANDO SE TERMINE ELDEVELOPMENT
    path('csrf_token/', user_views.csrf_token_view, name = "csrf"),

    # COMENTAR CUANDO SE PASE A FLUTTER
    path('login/', user_views.login_view, name="login"),
    path('register/', user_views.register_view, name="register"),
    path('logout/', user_views.logout_view, name="logout"),

    path('crear_actualizar_objeto/', catalog_views.crear_actualizar_objeto_view, name="crear_actualizar_objeto"),
    path('borrar_objeto/<nombre_objeto>/', catalog_views.borrar_objeto_view, name="borrar_objeto"),
    path('mostrar_catalogo/', catalog_views.mostrar_objetos, name="mostrar_objetos"),

    path('rna_train/<nombre_objeto>/', rna_views.entrenar_rna_view, name="rna_train"),
    path('rna_test/<nombre_objeto>/', rna_views.buscar_rna_view, name="rna_test"),
    path('rna_get_estado/', rna_views.get_estado_rna_view, name="rna_get_estado"),
    path('rna_get_estado/', rna_views.get_estado_rna_view, name="rna_get_estado"),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'),
         name='password_change'),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
         name='password_reset_complete'),


]
