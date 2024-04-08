from django.urls import path
from .views import mainbase

app_name = 'main'
urlpatterns = [
    path('', mainbase, name='home'),
]