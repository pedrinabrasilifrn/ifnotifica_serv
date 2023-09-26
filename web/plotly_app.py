from dash import Dash, dash_table, dcc, html, Input, Output, callback
import pandas as pd
from django_plotly_dash import DjangoDash
from web.models import Notificacao

notificacoes = Notificacao.objects.all()
df_tabela = pd.DataFrame(columns=['notificacao', 'sexo', 'clinica', 'cidade', 'estado', 'tipo de teste', 'resultado', 'data de notificação'])

# collect all the data for this dataframe that is referred in the columns above
for n in notificacoes:
    notificacao_atual = n.id
    sexo = n.atendimento.paciente.sexo
    clinica = n.atendimento.local.descricao
    cidade = n.atendimento.local.cidade.descricao
    estado = n.atendimento.local.cidade.estado
    tipo_de_teste = n.tipo_teste
    resultado = n.resultado
    data_de_notificacao = n.data_envio

    # create a dictionary with the data collected above
    data = {'notificacao': notificacao_atual, 'sexo': sexo, 'clinica': clinica, 'cidade': cidade, 'estado': estado, 'tipo de teste': tipo_de_teste, 'resultado': resultado, 'data de notificação': data_de_notificacao}

    # append the dictionary to the dataframe
    df_tabela.loc[len(df_tabela)] = data


app = DjangoDash('tabela_notificacoes')

app.layout = html.Div([
    dash_table.DataTable(
        id='tabela_notificacoes',
        columns=[{"name": i, "id": i} for i in df_tabela.columns],
        data=df_tabela.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
        style_table={
            'width': '100%',
            'margin': 'auto',
        },
    ),
    html.Div(id='datatable-interactivity-container')
    ],
)

@callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns')
)

def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]