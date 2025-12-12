from django.contrib import admin
from .models import *

admin.site.register(ServerSetting)
@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('contact_id', 'contact_name', 'pipeline_type', 'stage', 'created_at')
    search_fields = ('contact_id', 'contact_name', 'pipeline_type', 'stage')
    list_filter = ('pipeline_type', 'stage')
