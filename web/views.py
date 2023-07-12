from django.shortcuts import render

from web.models import Notificacao

# Create your views here.
def index(request):
    context = { 'lista' : Notificacao.objects.all()}
    return render(request, 'web/index.html', context=context)