import datetime
from django.shortcuts import render
from api.models import Machine


def index(request):
    template = 'mainapp/index.html'
    result = []
    for m in Machine.objects.all():
        worktime = datetime.timedelta(0)
        for i in range(m.records.count()):
            if i < m.records.count() - 1:
                states = {ii.name for ii in m.records.all()[i].states.all()}
                if not states or states == {"yellow","green"}:
                    worktime += m.records.all()[i + 1].datetime - m.records.all()[i].datetime
        freetime = datetime.timedelta(0)
        for i in range(m.records.count()):
            if i < m.records.count() - 1:
                states = {ii.name for ii in m.records.all()[i].states.all()}
                if states and states != {"yellow", "green"}:
                    freetime += m.records.all()[i + 1].datetime - m.records.all()[i].datetime
        if (worktime + freetime).seconds > 0:
            productivity = worktime.seconds * 100 // (worktime + freetime).seconds
        else:
            productivity = 0
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
            'worktime': worktime.seconds // 3600,
            'freetime': freetime.seconds // 3600,
            'count': m.records.count(),
            'productivity': productivity,
            'connected': connected,
            'pic': pic,
        })
    context = {
        'machines': result,
    }
    return render(request, template, context)
