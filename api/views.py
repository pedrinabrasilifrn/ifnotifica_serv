from django.shortcuts import render
from rest_framework import viewsets
from web.models import Paciente, Atendimento, Notificacao
from api.serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout,authenticate, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status
from datetime import date
from web.models import UnidadeBasica, Paciente, Cidade,Bairro

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

@api_view(['POST'])
@permission_classes([AllowAny])
def autenticar(request):
    print("Recebeu a requisição de autenticacao")
    username = request.data.get('usuario')
    senha = request.data.get('senha')
    usu = authenticate(request, username=username, password=senha)
    if usu:
        #Checa se usuario esta ativo, é necessario para o futuro, caso voce destive o usuario ele não ira mais logar
        if usu.is_active:
            login(request, usu)
            #token, created = Token.objects.get_or_create(user=usu)
            return JsonResponse({'token': "ifnotifica23200930"}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': "Usuário inativo."}, status=status.HTTP_401_UNAUTHORIZED)            

    else:
        return JsonResponse({'error': "CPF ou senha inválido(s)."}, status=status.HTTP_401_UNAUTHORIZED)            

import json
@api_view(['POST'])
def receber_notificacao(request):
    print("Recebeu a requisição de notificacao")
    token = request.data.get('token')
    if token == "ifnotifica23200930":
        notificacao = request.data.get('notificacao')
        notificacao = json.loads(notificacao)
        nova_n = Notificacao()
        nova_n.data_notificacao = notificacao["d_notificacao"]
        nova_n.tipo_teste = notificacao["tipo_teste"]    
        nova_n.estado_teste = notificacao["estado_teste"]
        nova_n.resultado = notificacao["resultado_teste"]
        if notificacao["assintomatico"] == "true":
             nova_n.assintomatico = True
        else:
             nova_n.assintomatico = False
        nova_n.sintomas = notificacao["sintomas"].split(",")
        nova_n.condicoes_especiais = notificacao["condicoes_especiais"].split(",")
        atendimento = notificacao["atendimento"]
        novo_a = Atendimento()
        novo_a.data_cadastro = atendimento["dt_cad"]
        novo_a.estrategia_atendimento = atendimento["estrategia"]
        ubs = UnidadeBasica.objects.filter(descricao__icontains = atendimento["local_teste"].strip()).first()
        if ubs is None:
            ubs = UnidadeBasica()
            ubs.descricao = atendimento["local_teste"]
            ubs.cidade = Cidade.objects.get(pk = 1)
            ubs = ubs.save()
        novo_a.local = ubs
        
        paciente = atendimento["paciente"]
        novo_p = Paciente.objects.filter(cpf = paciente["cpf"]).first()
        if novo_p is None:
            print("criou novo paciente")
            novo_p = Paciente()
            novo_p.cpf = paciente["cpf"]
            novo_p.cbo = paciente["cbo"]
            novo_p.nome = paciente["nome"]
            novo_p.data_nascimento = paciente["d_nascimento"]
            novo_p.sexo = paciente["sexo"]
            novo_p.cor = paciente["cor"]
            if paciente["tradicionalidade"]:
                novo_p.tradicionalidade = True
            else:
                novo_p.tradicionalidade = False
            novo_p.cep = paciente["cep"]    
            novo_p.logradouro = paciente["logradouro"]
            novo_p.numero = paciente["numero"]
            novo_p.complemento = paciente["complemento"]
            cidade = Cidade.objects.filter(estado = paciente["estado"], descricao__icontains=paciente["cidade"]).first()
            if cidade is None:
                cidade = Cidade()
                cidade.estado = paciente["estado"]
                cidade.descricao = paciente["cidade"]
                cidade = cidade.save()
            novo_p.cidade = cidade
            
            bairro = Bairro.objects.filter(cidade = cidade, descricao__icontains=paciente["bairro"]).first()
            if bairro is None:
                bairro = Bairro()
                bairro.cidade = cidade
                bairro.descricao = paciente["bairro"]
                bairro = bairro.save()
            novo_p.bairro = bairro
            novo_p.telefone1 =paciente["telefone1"]
            novo_p.telefone2 =paciente["telefone2"]
            novo_p.email = paciente["email"]
            novo_p.save()
        paciente = novo_p
        novo_a.paciente = paciente

        novo_a.save()
        atendimento = novo_a

        nova_n.atendimento = atendimento
        nova_n.save()        
        
        return JsonResponse({'msg': "Notificação enviada com sucesso"}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': "Não autorizado."}, status=status.HTTP_401_UNAUTHORIZED)            
