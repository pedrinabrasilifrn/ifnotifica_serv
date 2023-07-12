from random import choice
from django.db import models

class Estado(models.TextChoices):
    AC = "AC", "Acre"
    AL = "AL", "Alagoas"
    AP = "AP", "Amapá"
    AM = "AM", "Amazonas"
    BA = "BA", "Bahia"
    CE = "CE", "Ceará"
    DF = "DF", "Distrito Federal"
    ES = "ES", "Espírito Santo"
    GO = "GO", "Goiás"
    MA = "MA", "Maranhão"
    MT = "MT", "Mato Grosso"
    MS = "MS", "Mato Grosso do Sul"
    MG = "MG", "Minas Gerais"
    PA = "PA", "Pará"
    PB = "PB", "Paraíba"
    PR = "PR", "Paraná"
    PE = "PE", "Pernambuco"
    PI = "PI", "Piauí"
    RJ = "RJ", "Rio de Janeiro"
    RN = "RN", "Rio Grande do Norte"
    RS = "RS", "Rio Grande do Sul"
    RO = "RO", "Rondônia"
    RR = "RR", "Roraima"
    SC = "SC", "Santa Catarina"
    SP = "SP", "São Paulo"
    SE = "SE", "Sergipe"
    TO = "TO", "Tocantins"

class Sexo(models.TextChoices):
    FEM = "F", "Feminino"
    MASC = "M", "Masculino"

class Cor(models.TextChoices):
    BRANCO = "BRAN", "Branco"
    PARDO = "PARD", "Pardo"
    AMARELO = "AMARELO", "Amarelo"

class Cidade(models.Model):
    descricao = models.CharField(verbose_name="Cidade", blank=False, null=False, max_length=255)
    estado = models.CharField(verbose_name="Estado", blank=False, null=False, choices= Estado.choices, max_length=255)

    def __str__(self):
        return f"{self.descricao}, {self.estado}"

class Bairro(models.Model):
    descricao = models.CharField(verbose_name="Bairro", blank=False, null=False, max_length=255)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.descricao}, {self.cidade}"

class UnidadeBasica(models.Model):
    #TODO: Criar entidade par ubs, toda ubs tem descricao e cidade
    pass

# Create your models here.
# Create your models here.
class Paciente(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=11)
    cbo = models.CharField(max_length=15)
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=10, choices=Sexo.choices)
    cor = models.CharField(max_length=20, choices = Cor.choices)
    tradicionalidade = models.BooleanField()
    cep = models.CharField(max_length=8)
    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100)
    bairro = models.ForeignKey(Bairro, on_delete=models.PROTECT)
    telefone1 = models.CharField(max_length=15)
    telefone2 = models.CharField(max_length=15)
    email = models.CharField(max_length=100)
    data_cadastro = models.DateField()
    
    def __str__(self) -> str:
        return f"{self.cpf}, {self.nome}"

class Atendimento(models.Model):
  estrategia_atendimento = models.CharField(max_length=100)
  local_atendimento = models.CharField(max_length=100) #TODO: mudar local_atendimento para chave estrangeiro com ubs
  paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
  data_cadastro = models.DateField()
  
  def __str__(self) -> str:
        return f"{self.paciente}, {self.local_atendimento}"
    
class Notificacao(models.Model):
  notificacao = models.AutoField(primary_key=True)
  data_notificacao = models.DateField()
  tipo_teste = models.CharField(max_length=100) #TODO: fazer como textchoice (dando as opcoes validas)
  estado_teste = models.CharField(max_length=100) #TODO: fazer como textchoice (dando as opcoes validas)
  assintomatico = models.BooleanField()
  sintomas = models.CharField(max_length=100)
  condicoes_especiais = models.CharField(max_length=100)
  atendimento = models.ForeignKey(Atendimento, on_delete=models.CASCADE)
  data_cadastro = models.DateField()
  data_envio = models.DateField()

  def __str__(self) -> str:
        return f"{self.atendimento.paciente}, {self.data_cadastro}"