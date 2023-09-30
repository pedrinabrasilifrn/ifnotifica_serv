from django.shortcuts import render
from django.db.models import Count
import plotly.express as px
import plotly.graph_objects as go
from web.models import Notificacao, UnidadeBasica, Atendimento, Paciente, Resultado, Sexo
import calendar
from . import plotly_app
import pandas as pd
from django.db.models import OuterRef, Subquery

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
        df_sexo  = pd.DataFrame(columns=[])
        sexos = [s[0] for s in Sexo.choices]
        resultados = [r[0] for r in Resultado.choices]
        resultados.append("N/A")
        df_sexo["resultado"] = resultados
        for s in sexos:
            df_sexo[s] = [notificacoes.filter(atendimento__paciente__sexo = s).filter(resultado = resultados[0]).count(),
                        notificacoes.filter(atendimento__paciente__sexo = s).filter(resultado = resultados[1]).count(),
                        notificacoes.filter(atendimento__paciente__sexo = s).filter(resultado = resultados[2]).count(),
                        notificacoes.filter(atendimento__paciente__sexo = s).filter(resultado = None).count()]

        df_mes  = pd.DataFrame(columns=[])
        lista = [calendar.month_name[n.data_cadastro.month] for n in notificacoes]
        print(lista)
        meses = list(set(lista))

        resultados = [r[0] for r in Resultado.choices]
        resultados.append("N/A")
        df_mes["resultado"] = resultados
        for m in meses:
            df_mes[m] = [notificacoes.filter(atendimento__paciente__sexo = s).filter(resultado = resultados[0]).count(),
                        notificacoes.filter(atendimento__paciente__sexo = s).filter(resultado = resultados[1]).count(),
                        notificacoes.filter(atendimento__paciente__sexo = s).filter(resultado = resultados[2]).count(),
                        notificacoes.filter(atendimento__paciente__sexo = s).filter(resultado = None).count()]

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
            y = [1 for notificacao in notificacoes],
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

        numero_de_notificacoes_assintomaticas_enviadas = px.bar(
            x = [notificacao.atendimento.paciente.sexo for notificacao in notificacoes if notificacao.assintomatico == True],
            y = [1 for notificacao in notificacoes if notificacao.assintomatico == True],
            labels = {'x':'sexo', 'y':'Notificações enviadas'},
            color = [notificacao.atendimento.paciente.sexo for notificacao in notificacoes if notificacao.assintomatico == True],
            title ='Número de notificações assintomaticas enviadas por sexo',
        )

        grafico1 = numero_de_notificacoes_por_mes.to_html()
        grafico2 = numero_de_notificacoes_por_sexo.to_html()
        grafico3 = numero_de_notificacos_positivas_por_estado.to_html()
        grafico4 = numero_de_notificacoes_assintomaticas_enviadas.to_html()

        context["grafico1"] =  grafico1
        context["grafico2"] = grafico2
        context["grafico3"] = grafico3
        context["grafico4"] = grafico4
        context["ultima_atualizacao"] =  ultima_atualizacao

    return render(request, 'web/index.html', context=context)

def sobre(request):
    return render(request, 'web/sobre.html')