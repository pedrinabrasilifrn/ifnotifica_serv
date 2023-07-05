from django.db import models

# Create your models here.
class Paciente(models.Model):
  id_paciente = models.AutoField(primary_key=True)
  cpf = models.CharField(max_length=11)
  cbo = models.CharField(max_length=15)
  nome = models.CharField(max_length=100)
  data_nascimento = models.DateField()
  sexo = models.CharField(max_length=10)
  cor = models.CharField(max_length=20)
  tradicionalidade = models.BooleanField()
  cep = models.CharField(max_length=8)
  logradouro = models.CharField(max_length=100)
  numero = models.CharField(max_length=10)
  complemento = models.CharField(max_length=100)
  bairro = models.CharField(max_length=100)
  estado = models.CharField(max_length=2)
  cidade = models.CharField(max_length=100)
  telefone1 = models.CharField(max_length=15)
  telefone2 = models.CharField(max_length=15)
  email = models.CharField(max_length=100)
  data_cadastro = models.DateField()

class Atendimento(models.Model):
  id_atendimento = models.AutoField(primary_key=True)
  estrategia_atendimento = models.CharField(max_length=100)
  local_atendimento = models.CharField(max_length=100)
  id_paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
  data_cadastro = models.DateField()

class Notificacao(models.Model):
  id_notificacao = models.AutoField(primary_key=True)
  data_notificacao = models.DateField()
  tipo_teste = models.CharField(max_length=100)
  estado_teste = models.CharField(max_length=100)
  assintomatico = models.BooleanField()
  sintomas = models.CharField(max_length=100)
  condicoes_especiais = models.CharField(max_length=100)
  id_atendimento = models.ForeignKey(Atendimento, on_delete=models.CASCADE)
  data_cadastro = models.DateField()
  data_envio = models.DateField()