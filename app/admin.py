from django.contrib import admin

# Register your models here.
from .models import Client, Appointment, Service

admin.site.register(Client)
admin.site.register(Appointment)
admin.site.register(Service)


