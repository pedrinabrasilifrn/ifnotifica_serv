from importlib.metadata import requires
from django import forms
from .models import CondicoesEspeciais, Notificacao, Sintomas

class NotificacaoForm(forms.ModelForm):
    condicoes_especiais = forms.MultipleChoiceField(
        choices=CondicoesEspeciais.choices, 
        required=False, 
        widget=forms.CheckboxSelectMultiple,
        label=Notificacao._meta.get_field("condicoes_especiais").verbose_name)

    sintomas = forms.MultipleChoiceField(
        choices=Sintomas.choices, 
        required=False, 
        widget=forms.CheckboxSelectMultiple, 
        label=Notificacao._meta.get_field("sintomas").verbose_name)
    
    
    
    class Meta:
        model = Notificacao
        fields = ["data_notificacao",
            "tipo_teste",
            "estado_teste" ,
            "resultado",
            "assintomatico",
            "sintomas",
            "condicoes_especiais",
            "atendimento",
            "data_cadastro",
            "data_envio"]
