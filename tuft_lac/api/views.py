import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .models import *

@csrf_exempt
def index(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest(content='Invalid JSON')
    if 'name' in data.keys() and 'state' in data.keys():
        try:
            last = Record.objects.filter(machine_id=Machine.objects.get(name=data['name'])).last()
            if not last or {i.name for i in last.states.all()} != set(data['state']):
                record = Record.objects.create(machine=Machine.objects.get(name=data['name']))
                states = []
                for i in data['state']:
                    record.states.add(State.objects.get(name=i))
                record.save()
            elif {i.name for i in last.states.all()} == set(data['state']):
                last.save()
            return JsonResponse({'result': 'Success'})
        except ObjectDoesNotExist:
            return HttpResponseBadRequest(content='Wrong name or state')
    else:
        return HttpResponseBadRequest(content='Missing name or state')

