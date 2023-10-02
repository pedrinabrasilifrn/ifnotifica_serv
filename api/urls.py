from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from api.views import *

urlpatterns = [
    path('login', autenticar, name="login"),
    path('notificar', receber_notificacao, name="notificar")
]
