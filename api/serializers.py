from django.contrib.auth.models import User, Group
from rest_framework import serializers
from modelos.models import Paciente, Atendimento, Notificacao

# class de paciente
class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente 
        fields = ['id_paciente', 'cpf', 'cbo', 'nome', 'data_nascimento', 'sexo', 'cor', 'tradicionalidade', 'cep', 'logradouro', 'numero', 'complemento', 'bairro', 'estado', 'cidade', 'telefone1', 'telefone2', 'email', 'data_cadastro']

        # desativa o required do cbo
        extra_kwargs = {'cbo': {'required': False}} 

# class de atendimento
class AtendimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atendimento
        fields = ['id_atendimento', 'estrategia_atendimento', 'local_atendimento', 'id_paciente', 'data_cadastro']

# class de notificacao
class NotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacao
        fields = ['id_notificacao', 'data_notificacao', 'tipo_teste', 'estado_teste', 'assintomatico', 'sintomas', 'condicoes_especiais', 'data_cadastro', 'data_envio', 'id_atendimento']

        # falta fazer um verificador de se a pessoa for assintomatica n poder botar sintomas/condicoes (nao sei fazer)

        # desativa o required das datas de cadastro e envio
        extra_kwargs = {
            'data_cadastro': {'required': False},
            'data_envio': {'required': False}
        } 
