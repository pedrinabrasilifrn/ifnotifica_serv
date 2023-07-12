from django.shortcuts import render
from rest_framework import viewsets
from web.models import Paciente, Atendimento, Notificacao
from api.serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# viewset de paciente
class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

# viewset de atendimento
class AtendimentoViewSet(viewsets.ModelViewSet):
    queryset = Atendimento.objects.all()
    serializer_class = AtendimentoSerializer

    # dá a opção de pegar o id do paciente pela atendimento
    @action(detail=True, methods=['get'])
    def paciente(self, request, pk=None):
        atendimento = get_object_or_404(Atendimento, pk=pk)
        paciente = Atendimento.id_paciente
        serializer = PacienteSerializer(Paciente)
        return Response(serializer.data)

# viewset de notificacao
class NotificacaoViewSet(viewsets.ModelViewSet):
    queryset = Notificacao.objects.all()
    serializer_class = NotificacaoSerializer

    # dá a opção de pegar o id do atendimento pela notificação
    @action(detail=True, methods=['get'])
    def atendimento(self, request, pk=None):
        notificacao = get_object_or_404(notificacao, pk=pk)
        atendimento = Notificacao.id_atendimento
        serializer = AtendimentoSerializer(Atendimento)
        return Response(serializer.data)