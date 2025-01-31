import datetime
from django.shortcuts import render
from api.models import Machine, State
from django.utils.timezone import now


def light_alert(request):

    def get_states(queryset):
        return {ii.name for ii in queryset.states.all()}

    template = 'mainapp/light_alert.html'
    result = []
    for m in Machine.objects.all():
        worktime = 0
        freetime = 0
        count = 0
        month_start = now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        records = m.records.filter(datetime__gte=month_start)
        last_states = None
        if records:
            last = m.records.filter(id__lt=records.first().id)
            if last:
                last_states = get_states(last.last())
                if not last_states or last_states == {"yellow", "green"}:
                    worktime += records[0].datetime.timestamp() - month_start.timestamp()
                else:
                    freetime += records[0].datetime.timestamp() - month_start.timestamp()
                    count += 1
            for i in range(records.count()):
                states = get_states(records.all()[i])
                if i == 0:
                    if not states or states == {"yellow", "green"}:
                        if records.count() > 1:
                            worktime += records[i+1].datetime.timestamp() - records[i].datetime.timestamp()
                        else:
                            worktime += now().timestamp() - records[i].datetime.timestamp()
                    else:
                        if not last:
                            count += 1
                        else:
                            if not last_states or last_states == {"yellow", "green"}:
                                count += 1
                        if records.count() > 1:
                            freetime += records[i+1].datetime.timestamp() - records[i].datetime.timestamp()
                        else:
                            freetime += now().timestamp() - records[i].datetime.timestamp()
                elif i != 0 and i + 1 == records.count():
                    if not states or states == {"yellow", "green"}:
                        worktime += now().timestamp() - records[i].datetime.timestamp()
                    else:
                        if not get_states(records.all()[i-1]) or get_states(records.all()[i-1]) == {"yellow", "green"}:
                            count += 1
                        freetime += now().timestamp() - records[i].datetime.timestamp()
                else:
                    if not states or states == {"yellow", "green"}:
                        worktime += records[i+1].datetime.timestamp() - records[i].datetime.timestamp()
                    else:
                        if not get_states(records.all()[i-1]) or get_states(records.all()[i-1]) == {"yellow", "green"}:
                            count += 1
                        freetime += records[i+1].datetime.timestamp() - records[i].datetime.timestamp()
        if worktime + freetime > 0:
            productivity = worktime * 100 // (worktime + freetime)
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
            'worktime': worktime // 3600,
            'freetime': freetime // 3600,
            'count': count,
            'productivity': productivity,
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
