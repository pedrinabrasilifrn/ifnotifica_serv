from django.shortcuts import render
from django.db.models import Count
import plotly.express as px
import plotly.graph_objects as go
from web.models import Atendimento, Notificacao, Paciente, Resultado, Sexo, UnidadeBasica 
import calendar
import pandas as pd
from . import plotly_app
from django.db.models import OuterRef, Subquery
# Create your views here.
def index(request):
    notificacoes = Notificacao.objects.all().select_related("atendimento", "atendimento__paciente")
    for n in notificacoes:
        print(n.atendimento.paciente.sexo)

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
        sexos = [n.get_sexo() for n in notificacoes]
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
        
        numero_de_notificacoes_por_mes = px.histogram(df_mes,
            x = meses,
            y = resultados,
            labels = {'x':'Mês', 'y':'Notificações cadastradas'},
            title ='Número de notificações por mês',
        )

        numero_de_notificacoes_por_mes.update_layout(
            xaxis=dict(title='Valores'),
            yaxis=dict(title='Resultados'),
        )
        
        numero_de_notificacoes_por_sexo = px.bar(df_sexo,
            x = sexos,
            y = resultados,
            labels = {'x':'reultado', 'y':'Número de Notificações'},            
            title ='Número de notificações por sexo',
            text=resultados
        )
        df = pd.DataFrame(notificacoes.values())
        df["sexo"] = [n.atendimento.paciente.sexo for n in notificacoes]
        numero_de_notificacoes_por_sexo = px.bar(df,
            x = "sexo",
            y =  "resultado",
            labels = {'x':'reultado', 'y':'Número de Notificações'},            
            title ='Número de notificações por sexo'
        )

        numero_de_notificacos_positivas_por_estado = px.bar(
            x = [notificacao.atendimento.paciente.cidade.estado for notificacao in notificacoes],
            y = [1 for notificacao in notificacoes],
            labels = {'x':'Estado', 'y':'Notificações positivas'},
            #color = [notificacao.atendimento.paciente.cidade.estado for notificacao in notificacoes if notificacao.resultado == 'REAGENTE'],
            color= [notificacao.resultado for notificacao in notificacoes],
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