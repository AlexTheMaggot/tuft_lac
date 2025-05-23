from django.contrib import admin
from .models import *


class RecordAdmin(admin.ModelAdmin):
    list_display = ['machine', 'get_states', 'datetime']
    list_filter = ['machine', 'datetime', 'states']


admin.site.register(Machine)
admin.site.register(State)
admin.site.register(Record, RecordAdmin)