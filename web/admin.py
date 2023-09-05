from django.contrib import admin
from web.models import Paciente, Atendimento, Notificacao,Cidade, Bairro, UnidadeBasica
from .forms import NotificacaoForm
# Register your models here.
admin.site.register(Paciente)
admin.site.register(Atendimento)

admin.site.register(Cidade)
admin.site.register(Bairro)
admin.site.register(UnidadeBasica)



from django import forms

class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ["id", "data_notificacao", "tipo_teste", "atendimento"]
    list_display_links = ["id"]
    form = NotificacaoForm
    
 
admin.site.register(Notificacao, NotificacaoAdmin)
    
    
    
