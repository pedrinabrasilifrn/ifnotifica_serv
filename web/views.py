from django.shortcuts import render
from django.db.models import Count

from web.models import Notificacao, UnidadeBasica 

# Create your views here.
def index(request):

    context = { 
        'lista' : Notificacao.objects.all(), 
        'casos_suspeitos' : Notificacao.objects.filter(resultado='INDETERMINADO').count(),
        'casos_confirmados' : Notificacao.objects.filter(resultado='REAGENTE').count(),
        'casos_descartados' : Notificacao.objects.filter(resultado='NAO_REAGENTE').count(),
        'ultima_atualizacao' : Notificacao.objects.latest('data_cadastro').data_cadastro,

        'ubs_mais_visitada' : UnidadeBasica.objects.all().annotate(num_atendimentos=Count('atendimento')).order_by('-num_atendimentos')[0],
    }

    return render(request, 'web/index.html', context=context)