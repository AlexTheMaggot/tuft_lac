import os
import sys
import django
import time
from django.utils.timezone import now, localtime
from django.db.models import Prefetch

sys.path.append('./tuft_lac')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tuft_lac.settings')
django.setup()

from api.models import *

while True:
    start_time = time.time()


    def get_states(record):
        return {state.name for state in record.states.all()}

    month_start = localtime(now()).replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    machines = Machine.objects.prefetch_related(
        Prefetch("records", queryset=Record.objects.filter(datetime__gte=month_start).order_by("datetime"))
    )

    for m in machines:
        worktime = 0
        freetime = 0
        count = 0
        records = list(m.records.all())
        record_count = len(records)

        if records:
            first_record = records[0]
            last_record_before_start = m.records.filter(datetime__lt=month_start).order_by("-datetime").first()

            last_states = get_states(last_record_before_start) if last_record_before_start else None

            if not last_states or last_states == {"yellow", "green"}:
                worktime += first_record.datetime.timestamp() - month_start.timestamp()
            else:
                freetime += first_record.datetime.timestamp() - month_start.timestamp()
                count += 1

            for i in range(record_count):
                current_states = get_states(records[i])

                if i == 0:
                    if not current_states or current_states == {"yellow", "green"}:
                        worktime += (records[i+1].datetime.timestamp() - records[i].datetime.timestamp()) if record_count > 1 else (localtime(now()).timestamp() - records[i].datetime.timestamp())
                    else:
                        if not last_record_before_start:
                            count += 1
                        else:
                            if not last_states or last_states == {"yellow", "green"}:
                                count += 1
                        freetime += (records[i+1].datetime.timestamp() - records[i].datetime.timestamp()) if record_count > 1 else (localtime(now()).timestamp() - records[i].datetime.timestamp())

                elif i + 1 == record_count:
                    if not current_states or current_states == {"yellow", "green"}:
                        worktime += localtime(now()).timestamp() - records[i].datetime.timestamp()
                    else:
                        if not get_states(records[i-1]) or get_states(records[i-1]) == {"yellow", "green"}:
                            count += 1
                        freetime += localtime(now()).timestamp() - records[i].datetime.timestamp()
                else:
                    if not current_states or current_states == {"yellow", "green"}:
                        worktime += records[i+1].datetime.timestamp() - records[i].datetime.timestamp()
                    else:
                        if not get_states(records[i-1]) or get_states(records[i-1]) == {"yellow", "green"}:
                            count += 1
                        freetime += records[i+1].datetime.timestamp() - records[i].datetime.timestamp()

        productivity = (worktime * 100 // (worktime + freetime)) if (worktime + freetime) > 0 else 0

        m.worktime = worktime // 3600
        m.freetime = freetime // 3600
        m.count = count
        m.productivity = productivity
        m.save()

    print(f"Execution time: {time.time() - start_time:.2f} sec")
