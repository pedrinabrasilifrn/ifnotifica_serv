from django.shortcuts import render
from django.db.models import Count
import plotly.express as px
import plotly.graph_objects as go
from web.models import Notificacao, UnidadeBasica 
import calendar

# Create your views here.
def index(request):
    notificacoes = Notificacao.objects.all()
    casos_suspeitos = Notificacao.objects.filter(resultado='INDETERMINADO').count()
    casos_confirmados = Notificacao.objects.filter(resultado='REAGENTE').count()
    casos_descartados = Notificacao.objects.filter(resultado='NAO_REAGENTE').count()
    
    ubs_mais_visitada = UnidadeBasica.objects.all().annotate(num_atendimentos=Count('atendimento')).order_by('-num_atendimentos')[0]
    
    context = { 
        'lista' : notificacoes, 
        'casos_suspeitos' : casos_suspeitos,
        'casos_confirmados' : casos_confirmados,
        'casos_descartados' : casos_descartados,
        'ubs_mais_visitada' : ubs_mais_visitada,
    }

    if len(notificacoes.values_list()) > 0:
        ultima_atualizacao = Notificacao.objects.latest('data_cadastro').data_cadastro
        
        numero_de_notificacoes_por_mes = px.bar(
            x = [calendar.month_name[notificacao.data_cadastro.month] for notificacao in notificacoes],
            y = [1 for notificacao in notificacoes],
            labels = {'x':'Mês', 'y':'Notificações cadastradas'},
            color= [notificacao.resultado for notificacao in notificacoes],
            title ='Número de notificações por mês',
        )

        numero_de_notificacoes_por_sexo = px.bar(
            x = [notificacao.atendimento.paciente.sexo for notificacao in notificacoes],
            labels = {'x':'Sexo', 'y':'Notificações enviadas'},
            color= [notificacao.atendimento.paciente.sexo for notificacao in notificacoes],
            title ='Número de notificações por sexo',
        )

        numero_de_notificacos_positivas_por_estado = px.bar(
            x = [notificacao.atendimento.paciente.cidade.estado for notificacao in notificacoes if notificacao.resultado == 'REAGENTE'],
            y = [1 for notificacao in notificacoes if notificacao.resultado == 'REAGENTE'],
            labels = {'x':'Estado', 'y':'Notificações positivas'},
            color = [notificacao.atendimento.paciente.cidade.estado for notificacao in notificacoes if notificacao.resultado == 'REAGENTE'],
            title ='Número de notificações positivas por estado',
        )

        # TODO: ajeitar histograma
        numero_de_notificacoes_por_idade_e_sexo = px.histogram(
            # TODO: Calcular a idade do paciente
            y = [notificacao.atendimento.paciente.sexo for notificacao in notificacoes],
            labels = {'x':'Idade', 'y':'Notificações enviadas'},
            color = [notificacao.atendimento.paciente.sexo for notificacao in notificacoes],
            title ='Número de notificações por idade e sexo',
        )

        # TODO: ajeitar barra
        numero_de_notificacoes_com_tal_teste = px.bar(
            x = [notificacao.tipo_teste for notificacao in notificacoes],
            labels = {'x':'Teste', 'y':'Notificações enviadas'},
            color = [notificacao.tipo_teste for notificacao in notificacoes],
            title ='Número de notificações por teste',
        )

        grafico1 = numero_de_notificacoes_por_mes.to_html()
        grafico2 = numero_de_notificacoes_por_sexo.to_html()
        grafico3 = numero_de_notificacos_positivas_por_estado.to_html()
        grafico4 = numero_de_notificacoes_por_idade_e_sexo.to_html()

        context["grafico1"] =  grafico1
        context["grafico2"] = grafico2
        context["grafico3"] = grafico3
        context["grafico4"] = grafico4
        context["ultima_atualizacao"] =  ultima_atualizacao

    return render(request, 'web/index.html', context=context)