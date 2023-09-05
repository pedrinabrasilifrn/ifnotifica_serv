from django.contrib import admin
from web.models import Paciente, Atendimento, Notificacao,Cidade, Bairro, UnidadeBasica
from .forms import NotificacaoForm
# Register your models here.

class PacienteAdmin(admin.ModelAdmin):
    list_display = ["id", "cpf", "nome", "sexo", "data_nascimento"]
    list_display_links = ["id", "cpf"]

admin.site.register(Paciente,PacienteAdmin)

class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ["id", "estrategia_atendimento", "local", "paciente", "data_cadastro"]
    list_display_links = ["id"]

admin.site.register(Atendimento,AtendimentoAdmin)

class CidadeAdmin(admin.ModelAdmin):
    list_display = ["id", "descricao", "estado"]
    list_display_links = ["id", "descricao"]

admin.site.register(Cidade,CidadeAdmin)

class BairroAdmin(admin.ModelAdmin):
    list_display = ["id", "descricao", "cidade"]
    list_display_links = ["id", "descricao"]

admin.site.register(Bairro,BairroAdmin)

class UnidadeBasicaAdmin(admin.ModelAdmin):
    list_display = ["id", "descricao", "cidade"]
    list_display_links = ["id", "descricao"]
    
admin.site.register(UnidadeBasica,UnidadeBasicaAdmin)


class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ["id", "data_notificacao", "tipo_teste", "atendimento"]
    list_display_links = ["id"]
    form = NotificacaoForm
 
admin.site.register(Notificacao, NotificacaoAdmin)
    
    
    
