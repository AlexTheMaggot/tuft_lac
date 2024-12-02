from django.shortcuts import render
from api.models import Machine


def index(request):
    template = 'mainapp/index.html'
    context = {
        'machines': Machine.objects.all(),
    }
    return render(request, template, context)
