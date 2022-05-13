from django.urls import path
from .views import *
app_name = 'makan'

urlpatterns = [
    path('read_makan_admin/', read_makan_admin, name='read_makan_admin'),
    path('read_makan_pemain/', read_makan_pemain, name='read_makan_pemain')
]