__author__ = 'pgcd'
from scheduled_blocks.models import ScheduledBlock
from django.contrib import admin

class ScheduledBlockAdmin(admin.ModelAdmin):
    list_display = ['name','display_from','display_to','template_name','event_name']

admin.site.register(ScheduledBlock, ScheduledBlockAdmin)