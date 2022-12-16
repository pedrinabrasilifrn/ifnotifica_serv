from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from api.views import *


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# routers das tabelas
router.register(r'pacientes', pacienteViewSet)
router.register(r'atendimentos', atendimentoViewSet)
router.register(r'notificacoes', notificacaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
