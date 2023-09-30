from django.contrib.auth.models import User, Group
from rest_framework import serializers
from web.models import Paciente, Atendimento, Notificacao

# class de paciente
class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente 
        fields = ['cpf', 'cbo', 'nome', 'data_nascimento', 'sexo', 'cor', 'tradicionalidade', 'cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'telefone1', 'telefone2', 'email', 'data_cadastro']

# class de atendimento
class AtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atendimento
        fields = ['estrategia_atendimento', 'local', 'paciente', 'data_cadastro']

# class de notificacao
class NotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacao
        fields = ['data_notificacao', 'tipo_teste', 'estado_teste', 'resultado','assintomatico', 'sintomas', 'condicoes_especiais', 'data_cadastro', 'data_envio', 'atendimento']
