from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path('login/',login_view, name="login"),
    path('logout/', logout_view, name='logout'),
    path('update-theme/', update_theme, name='update_theme'),
    path('sync-opportunities/', sync_opportunities_view, name='sync_opportunities'),
    path('update-opportunities/', update_opportunities_view, name='update_opportunities'),

]
