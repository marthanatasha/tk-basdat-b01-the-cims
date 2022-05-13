from django.urls import path
from .views import *
app_name = 'makanan'

urlpatterns = [
    path('read_makanan_admin/', read_makanan_admin, name='read_makanan_admin'),
    path('read_makanan_pemain/', read_makanan_pemain, name='read_makanan_pemain')
]