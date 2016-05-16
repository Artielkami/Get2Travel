from django.contrib import admin
from .models import Ticket, Airport, MiddlePort, DomesticRegion, Carrier

# Register your models here.
admin.site.register(Ticket)
admin.site.register(Airport)
admin.site.register(DomesticRegion)
admin.site.register(MiddlePort)
admin.site.register(Carrier)