from django.contrib import admin
from .models import (CaseWorker, YoungPerson, Offence, 
                     Intervention, CourtHearing, HearingOffence)

admin.site.register(CaseWorker)
admin.site.register(YoungPerson)
admin.site.register(Offence)
admin.site.register(Intervention)
admin.site.register(CourtHearing)
admin.site.register(HearingOffence)