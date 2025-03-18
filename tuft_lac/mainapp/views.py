import datetime
from django.shortcuts import render
from api.models import Machine, State


def light_alert(request):
    template = 'mainapp/light_alert.html'
    result = []
    for m in Machine.objects.all():
        connected = False
        if m.records.last():
            td = datetime.datetime.now(tz=datetime.timezone.utc) - m.records.last().updated
            if td.seconds < 10:
                connected = True
        pic = 'NC.png'
        if m.records.last():
            if not {i.name for i in m.records.last().states.all()}:
                pic = 'IDL'
            elif {i.name for i in m.records.last().states.all()} == {'red'}:
                pic = 'R'
            elif {i.name for i in m.records.last().states.all()} == {'red', 'green'}:
                pic = 'RG'
            elif {i.name for i in m.records.last().states.all()} == {'red', 'yellow'}:
                pic = 'RY'
            elif {i.name for i in m.records.last().states.all()} == {'red', 'green', 'yellow'}:
                pic = 'RYG'
            elif {i.name for i in m.records.last().states.all()} == {'yellow', 'green'}:
                pic = 'YG'
        result.append({
            'id': m.id,
            'worktime': m.worktime,
            'freetime': m.freetime,
            'count': m.count,
            'productivity': m.productivity,
            'connected': connected,
            'pic': pic,
        })
    context = {
        'machines': result,
    }
    return render(request, template, context)


def index(request):
    template = 'mainapp/index.html'
    return render(request, template)


def phone_number(request):
    template = 'mainapp/phone_number.html'
    return render(request, template)
