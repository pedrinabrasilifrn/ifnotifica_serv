from django.shortcuts import render
from rest_framework import viewsets
from api.models import paciente, atendimento, notificacao
from api.serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# viewset de paciente
class pacienteViewSet(viewsets.ModelViewSet):
    queryset = paciente.objects.all()
    serializer_class = pacienteSerializer

# viewset de atendimento
class atendimentoViewSet(viewsets.ModelViewSet):
    queryset = atendimento.objects.all()
    serializer_class = atendimentoSerializer

    # dá a opção de pegar o id do paciente pela atendimento
    @action(detail=True, methods=['get'])
    def paciente(self, request, pk=None):
        atendimento = get_object_or_404(atendimento, pk=pk)
        paciente = atendimento.id_paciente
        serializer = pacienteSerializer(paciente)
        return Response(serializer.data)

# viewset de notificacao
class notificacaoViewSet(viewsets.ModelViewSet):
    queryset = notificacao.objects.all()
    serializer_class = notificacaoSerializer

    # dá a opção de pegar o id do atendimento pela notificação
    @action(detail=True, methods=['get'])
    def atendimento(self, request, pk=None):
        notificacao = get_object_or_404(notificacao, pk=pk)
        atendimento = notificacao.id_atendimento
        serializer = atendimentoSerializer(atendimento)
        return Response(serializer.data)