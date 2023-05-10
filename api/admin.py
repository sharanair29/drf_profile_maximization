from django.contrib import admin
from .models import Contracts
# Register your models here.


class ContractsAdmin(admin.ModelAdmin):
    list_display = ['name', 'start', 'duration', 'price']


admin.site.register(Contracts, ContractsAdmin)
