from django.contrib import admin
from web.models import Paciente, Atendimento, Notificacao,Cidade, Bairro

# Register your models here.
admin.site.register(Paciente)
admin.site.register(Atendimento)
admin.site.register(Notificacao)
admin.site.register(Cidade)
admin.site.register(Bairro)
