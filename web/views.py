from django.shortcuts import render
from django.db.models import Count
import plotly.express as px
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
            labels= {'x':'Mês', 'y':'Notificações cadastradas'},
            title='Número de notificações por mês',
        )

        numero_de_notificacoes_por_sexo = px.bar(
            x = [notificacao.atendimento.paciente.sexo for notificacao in notificacoes],
            y = [1 for notificacao in notificacoes],
            labels= {'x':'Sexo', 'y':'Notificações enviadas'},
            title='Número de notificações por sexo',
        )

        grafico1 = numero_de_notificacoes_por_mes.to_html()
        grafico2 = numero_de_notificacoes_por_sexo.to_html()

        context["grafico1"] =  grafico1
        context["grafico2"] = grafico2
        context["ultima_atualizacao"] =  ultima_atualizacao

    return render(request, 'web/index.html', context=context)