from django.contrib import admin
from web.models import Paciente, Atendimento, Notificacao,Cidade, Bairro, UnidadeBasica
from .forms import NotificacaoForm
# Register your models here.
admin.site.register(Paciente)
admin.site.register(Atendimento)

admin.site.register(Cidade)
admin.site.register(Bairro)
admin.site.register(UnidadeBasica)



    
@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    form = NotificacaoForm
