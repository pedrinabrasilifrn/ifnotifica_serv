from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from api.views import *


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# routers das tabelas
router.register(r'pacientes', PacienteViewSet)
router.register(r'atendimentos', AtendimentoViewSet)
router.register(r'notificacoes', NotificacaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
