from django.shortcuts import render
from django.db.models import Count
import plotly.express as px
from web.models import Notificacao, UnidadeBasica 

# Create your views here.
def index(request):
    notificacoes = Notificacao.objects.all()
    casos_suspeitos = Notificacao.objects.filter(resultado='INDETERMINADO').count()
    casos_confirmados = Notificacao.objects.filter(resultado='REAGENTE').count()
    casos_descartados = Notificacao.objects.filter(resultado='NAO_REAGENTE').count()
    ultima_atualizacao = Notificacao.objects.latest('data_cadastro').data_cadastro
    ubs_mais_visitada = UnidadeBasica.objects.all().annotate(num_atendimentos=Count('atendimento')).order_by('-num_atendimentos')[0]

    figura1 = px.line(
        x = [notificacao.data_envio for notificacao in notificacoes],
        # numero de infeccoes por data
        y = [notificacao.atendimento.paciente.count() for notificacao in notificacoes],
    )

    grafico1 = figura1.to_html()

    context = { 
        'lista' : notificacoes, 
        'casos_suspeitos' : casos_suspeitos,
        'casos_confirmados' : casos_confirmados,
        'casos_descartados' : casos_descartados,
        'ultima_atualizacao' : ultima_atualizacao,

        'ubs_mais_visitada' : ubs_mais_visitada,
        'grafico1' : grafico1,
    }

    return render(request, 'web/index.html', context=context)