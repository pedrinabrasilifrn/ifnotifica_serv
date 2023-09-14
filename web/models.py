from django.db import models
from django.core.validators import MaxValueValidator,  MinLengthValidator
from datetime import date
from multiselectfield import MultiSelectField

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

class EstrategiaAtendimento(models.TextChoices):
    DIAGNOSTICO_SINTOMATICO = "DIAGNOSTICO_SINTOMATICO", "Diagnóstico assistencial"
    BUSCA_ATIVA_ASSINTOMATICO = "BUSCA_ATIVA_ASSINTOMATICO", "Busca ativa de assintomático"
    TRIAGEM_POPULACAO_ESPECIFICA = "TRIAGEM_POPULACAO_ESPECIFICA", "Triagem de população específica"

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

class Sintomas(models.TextChoices):
    CORIZA = "CORIZA", "Coriza"
    FEBRE = "FEBRE", "Febre"
    DOR_DE_CABECA = "DOR_DE_CABECA", "Dor de cabeça"
    DOR_DE_GARGANTA = "DOR_GARGANTA", "Dor de garganta"
    DISTURBIOS_GUSTATIVOS = "DISTURBIOS_GUSTATIVOS", "Distúrbios gustativos"
    DISPNEIA = "DISPNEIA", "Dispneia"
    DISTURBIOS_OLFATIVOS = "DISTURBIOS_OLFATIVOS", "Distúrbios olfativos"
    TOSSE = "TOSSE", "Tosse"
    OUTROS = "OUTROS", "Outros"

class CondicoesEspeciais(models.TextChoices):
    DOENCA_RESPIRATORIA = "DOENCA_RESPIRATORIA", "Doenças respiratória crônica"
    DOENCA_RENAL = "DOENCA_RENAL", "Doenças renal crônica em estagio avançado"
    DOENCA_CROMOSSOMICA = "DOENCA_CROMOSSOMICA", "Doenças cromossômicas ou estado de fragilidade imunológica"
    DOENCA_CARDIACA = "DOENCA_CARDIOVASCULAR", "Doença cardíacas crônicas"
    DOENCA_PUERPERA = "DOENCA_PUERPERA", "Puérpera (até 45 dias do parto)"
    IMUNOSSUPRESSAO = "IMUNOSSUPRESSAO", "Imunossupressão"
    DIABETES = "DIABETES", "Diabetes"
    GESTANTE = "GESTANTE", "Gestante"
    OBESIDADE = "OBESIDADE", "Obesidade"
    OUTROS = "OUTROS", "Outros"

class Cidade(models.Model):
    descricao = models.CharField(verbose_name="Cidade", blank=False, null=False, max_length=255, validators=[MinLengthValidator(3)])
    estado = models.CharField(verbose_name="Estado", blank=False, null=False, choices= Estado.choices, max_length=255)

    def __str__(self):
        return f"{self.descricao} - {self.estado}"
    
    class Meta:
        verbose_name = 'Cidade'
        verbose_name_plural = 'Cidades'

class Bairro(models.Model):
    descricao = models.CharField(verbose_name="Bairro", blank=False, null=False, max_length=255, validators=[MinLengthValidator(3)])
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.descricao}, {self.cidade}"
    
    class Meta:
        verbose_name = 'Bairro'
        verbose_name_plural = 'Bairros'
    

class UnidadeBasica(models.Model):
    descricao = models.CharField(verbose_name="Unidade basica", blank=False, null=False, max_length=128, validators=[MinLengthValidator(3)])
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.descricao}, {self.cidade}"
    
    class Meta:
        verbose_name = 'UBS'
        verbose_name_plural = 'UBS´s'


class Paciente(models.Model):
    cpf = models.CharField(max_length=11, blank=False, null=False, validators=[MinLengthValidator(11)], unique=True)
    cbo = models.CharField(max_length=15, blank=True, null=False,  validators=[MinLengthValidator(4)])
    nome = models.CharField(max_length=128, blank=False, null=False,  validators=[MinLengthValidator(12)])
    data_nascimento = models.DateField(validators=[MaxValueValidator(date.today)])
    sexo = models.CharField(max_length=10, blank=False, null=False, choices=Sexo.choices)
    cor = models.CharField(max_length=20, blank=False, null=False, choices=Cor.choices)
    tradicionalidade = models.BooleanField(blank=False, null=False, default=False)
    cep = models.CharField(max_length=8, blank=False, null=False, validators=[MinLengthValidator(7)])
    logradouro = models.CharField(max_length=128, blank=True, null=False)
    numero = models.CharField(max_length=10, blank=True, null=False, validators=[MinLengthValidator(1)])
    complemento = models.CharField(max_length=128, blank=True, null=False)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    bairro = models.ForeignKey(Bairro, on_delete=models.PROTECT)
    telefone1 = models.CharField(max_length=15, blank=False, null=False, validators=[MinLengthValidator(9)])
    telefone2 = models.CharField(max_length=15, blank=True, null=False, validators=[MinLengthValidator(9)])
    email = models.EmailField(max_length=128, blank=False, null=False)
    data_cadastro = models.DateField(blank=False, null=False, default=date.today, validators=[MaxValueValidator(date.today)])

    def __str__(self) -> str:
        return f"{self.cpf}, {self.nome}"

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

class Atendimento(models.Model):
    estrategia_atendimento = models.CharField(max_length=128, choices=EstrategiaAtendimento.choices)
    local = models.ForeignKey(UnidadeBasica, on_delete=models.PROTECT)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data_cadastro = models.DateField(blank=False, null=False, default=date.today, validators=[MaxValueValidator(date.today)])

    def __str__(self) -> str:
        return f"{self.paciente}, {self.local}, {self.data_cadastro}"
    
    class Meta:
        verbose_name = 'Atendimento'
        verbose_name_plural = 'Atendimentos'


class Notificacao(models.Model):
    data_notificacao = models.DateField(default=date.today)
    tipo_teste = models.CharField(max_length=128, blank=False, null=False, choices=TipoTeste.choices) 
    estado_teste = models.CharField(max_length=128, blank=False, null=False, choices=EstadoTeste.choices) 
    resultado = models.CharField(max_length=128, null=True,  blank=True,  choices=Resultado.choices) 
    assintomatico = models.BooleanField(default=False)
    sintomas = MultiSelectField("Sintomas", choices = Sintomas.choices, max_length=500, null=True)
    condicoes_especiais = MultiSelectField("Condições Especiais", choices = CondicoesEspeciais.choices, max_length=500 , null=True)
    atendimento = models.ForeignKey(Atendimento, on_delete=models.CASCADE)
    data_cadastro = models.DateField(default=date.today, validators=[MaxValueValidator(date.today)])
    data_envio = models.DateField(validators=[MaxValueValidator(date.today)], null=True,   blank=True)        
    

    def get_sexo(self):
        return self.atendimento.paciente.sexo

    def __str__(self) -> str:
        return f"{self.atendimento.paciente}, {self.data_cadastro}"
    
    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'