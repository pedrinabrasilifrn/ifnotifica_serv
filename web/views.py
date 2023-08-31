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
    ultima_atualizacao = Notificacao.objects.latest('data_cadastro').data_cadastro
    ubs_mais_visitada = UnidadeBasica.objects.all().annotate(num_atendimentos=Count('atendimento')).order_by('-num_atendimentos')[0]

    numero_de_notificacoes_por_mes = px.bar(
        x = [calendar.month_name[notificacao.data_envio.month] for notificacao in notificacoes],
        y = [1 for notificacao in notificacoes],
        labels= {'x':'Mês', 'y':'Notificações enviadas'},
        title='Número de notificações por mês'
    )

    numero_de_notificacoes_por_sexo = px.bar(
        x = [notificacao.atendimento.paciente.sexo for notificacao in notificacoes],
        y = [1 for notificacao in notificacoes],
        labels= {'x':'Sexo', 'y':'Notificações enviadas'},
        title='Número de notificações por sexo'
    )

    grafico1 = numero_de_notificacoes_por_mes.to_html()
    grafico2 = numero_de_notificacoes_por_sexo.to_html()

    context = { 
        'lista' : notificacoes, 
        'casos_suspeitos' : casos_suspeitos,
        'casos_confirmados' : casos_confirmados,
        'casos_descartados' : casos_descartados,
        'ultima_atualizacao' : ultima_atualizacao,

        'ubs_mais_visitada' : ubs_mais_visitada,
        'grafico1' : grafico1,
        'grafico2' : grafico2,
    }

    return render(request, 'web/index.html', context=context)