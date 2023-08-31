from django import forms
from .models import Notificacao

class NotificacaoForm(forms.ModelForm):

    class Meta:
        model = Notificacao
        fields = '__all__'
        widgets = {
            'condicoes_especiais': forms.CheckboxSelectMultiple,
            'sintomas': forms.CheckboxSelectMultiple,
        }

    def clean_condicoes_especiais(self):
        data = self.cleaned_data["condicoes_especiais"]
        return data
        
    def clean_sintomas(self):
        data = self.cleaned_data["sintomas"]
        return data

    
