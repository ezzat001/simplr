from django.db import models
from django.core.cache import cache


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ServerSetting(TimestampMixin):
    system_name = models.CharField(max_length=255, default="Zeo ERP")
    system_subtitle = models.CharField(max_length=255, blank=True, null=True, help_text="Optional subtitle under the system name")
    
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    favicon = models.ImageField(upload_to='favicons/', blank=True, null=True)

    geo_api_key = models.CharField(max_length=255, blank=True, null=True, help_text="API Key for Geocoding services")
    
    support_email = models.EmailField(blank=True, null=True)
    support_phone = models.CharField(max_length=50, blank=True, null=True)

    re_lead_form = models.BooleanField(default=True)
    roofing_lead_form = models.BooleanField(default=True)
    solar_lead_form = models.BooleanField(default=True)
    
    primary_color = models.CharField(max_length=20, blank=True, null=True, help_text="Hex or color name (e.g. #007bff)")
    footer_text = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete('system_settings') 
    def __str__(self):
        return self.system_name or "ERP System"
    





class Opportunity(models.Model):
    PIPELINE_CHOICES = [
        ('wholesaling', 'Wholesaling'),
        ('land', 'Land'),
        ('longterm', 'Long-Term'),
        ('new_leads', 'New Leads'),
    ]

    contact_id = models.CharField(max_length=255, unique=True)
    contact_name = models.CharField(max_length=255, blank=True, null=True)

    pipeline_id = models.CharField(max_length=255, blank=True, null=True)
    pipeline_type = models.CharField(max_length=50, choices=PIPELINE_CHOICES, default='wholesaling')
    stage = models.CharField(max_length=255, blank=True, null=True)  

    address = models.TextField(blank=True, null=True)

    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.contact_name} ({self.contact_id}) - {self.pipeline_type}"
