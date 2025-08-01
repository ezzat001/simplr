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
    


