from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('escaner/', views.vista_escaner, name='escaner'),
    path('historial/', views.historial_acceso, name='historial'),
    path('api/validar/<str:rut>/', views.validar_qr, name='validar_qr'),
    path('privacidad/', views.politica_privacidad, name='privacidad'),
]