from django.contrib import admin
from .models import *


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('id','name',
                    'created_at','updated_at', 'source_type', 'active')  # Add your desired fields here
    search_fields = ('name',)  # Optional: adds a search box
    list_filter = ('source_type','active')


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('id','name',
                    'created_at','updated_at', 'agents_count','daily_leads','campaign_type', 'status','active')  # Add your desired fields here
    search_fields = ('name',)  # Optional: adds a search box
    list_filter = ('status', 'campaign_type','active')

@admin.register(Lead)
class LeadnAdmin(admin.ModelAdmin):
    list_display = ('id','name',
                    'created_at','updated_at', 'campaign', 'status','active')  # Add your desired fields here
    search_fields = ('name',)  # Optional: adds a search box
    list_filter = ('status', 'campaign','active')