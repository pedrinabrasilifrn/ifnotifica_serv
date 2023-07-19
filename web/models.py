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
    PRETO = "PRETO", "Preto"
    INDIGINA = "INDIGINA", "Indígina"
    IGNORADO = "IGNORADO", "Ignorado"

class TipoTeste(models.TextChoices):
    RT_QPCR = "RT-QCPR", "Teste molecular em tempo real - RT-PCR"
    RT_LAMP = "RT-LAMP", "Teste molecular de amplianção isotermica - RT-LAMP"
    TESTE_RAPIDO = "ANTIGENO", "Teste rapido com Aitígeno"
 
class EstadoTeste(models.TextChoices):
    SOLICITADO = "SOLICITADO", "Teste solicitado"
    COLETADO = "COLETADO", "Teste coletado"
    CONCLUIDO = "CONCLUIDO", "Teste concluido" 
    NAO_SOLICITADO = "NAO_SOLICITADO", "Teste não solicitado"

class Resultado(models.TextChoices):
    REAGENTE = "REAGENTE", "Resultado positivo"
    NAO_REAGENTE = "NAO_REAGENTE", "Resultado negativo"
    INDETERMINADO = "INDETERMINADO", "Resultado indeterminado" 

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
    descricao = models.CharField(verbose_name="Unidade basica", blank=False, null=False, max_length=128)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.descricao}, {self.cidade}"


class Paciente(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=11, blank=False, null=False)
    cbo = models.CharField(max_length=15, blank=True, null=False)
    nome = models.CharField(max_length=100, blank=False, null=False)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=10, choices=Sexo.choices)
    cor = models.CharField(max_length=20, choices = Cor.choices)
    tradicionalidade = models.BooleanField(blank=False, null=False)
    cep = models.CharField(max_length=8, blank=False, null=False)
    logradouro = models.CharField(max_length=100, blank=True, null=False)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100)
    bairro = models.ForeignKey(Bairro, on_delete=models.PROTECT)
    telefone1 = models.CharField(max_length=15, blank=False, null=False)
    telefone2 = models.CharField(max_length=15, blank=False, null=False)
    email = models.EmailField(max_length=100, blank=False, null=False)
    data_cadastro = models.DateField()
    
    def __str__(self) -> str:
        return f"{self.cpf}, {self.nome}"

class Atendimento(models.Model):
    estrategia_atendimento = models.CharField(max_length=100, blank=False, null=False)
    local = models.ForeignKey(UnidadeBasica, on_delete=models.PROTECT)  #TODO: mudar local_atendimento para chave estrangeiro com ubs
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data_cadastro = models.DateField(blank=False, null=False)
  
    def __str__(self) -> str:
        return f"{self.paciente}, {self.local}"
    
class Notificacao(models.Model):
    data_notificacao = models.DateField()
    tipo_teste = models.CharField(max_length=100) #TODO: fazer como textchoice (dando as opcoes validas)
    estado_teste = models.CharField(max_length=100) #TODO: fazer como textchoice (dando as opcoes validas)
    resultado = models.CharField(max_length=100) #TODO: fazer como textchoice (dando as opcoes validas)
    assintomatico = models.BooleanField()
    sintomas = models.CharField(max_length=100)
    condicoes_especiais = models.CharField(max_length=100)
    atendimento = models.ForeignKey(Atendimento, on_delete=models.CASCADE)
    data_cadastro = models.DateField()
    data_envio = models.DateField()

    def __str__(self) -> str:
        return f"{self.atendimento.paciente}, {self.data_cadastro}"