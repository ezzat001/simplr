from django.contrib import admin
from .models import *


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('id','name',
                    'created_at','updated_at', 'source_type', 'active')  
    search_fields = ('name',)   
    list_filter = ('source_type','active')


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('id','name',
                    'created_at','updated_at', 'agents_count','daily_leads','campaign_type', 'status','active')  
    search_fields = ('name',)  
    list_filter = ('status', 'campaign_type','active')

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('id','name',
                    'created_at','updated_at', 'campaign', 'status','active')   
    search_fields = ('name',)   
    list_filter = ('status', 'campaign','active')


@admin.register(RealEstateLead)
class RELeadAdmin(admin.ModelAdmin):
    search_fields = ('lead',) 


@admin.register(RoofingLead)
class RoofingLeadAdmin(admin.ModelAdmin):
    search_fields = ('lead',)  

@admin.register(CustomLead)
class CustomLeadAdmin(admin.ModelAdmin):
    search_fields = ('lead',)  


@admin.register(CustomForm)
class CustomFormAdmin(admin.ModelAdmin):
    list_display = ('id','name',
                    'created_at','updated_at',  'active')
    search_fields = ('name',)

@admin.register(CustomFormField)
class CustomFormFieldAdmin(admin.ModelAdmin):
    list_display = ('id','label',
                    'created_at','updated_at', 'field_type','form','order',  'active')
    search_fields = ('name',)
