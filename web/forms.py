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
    
