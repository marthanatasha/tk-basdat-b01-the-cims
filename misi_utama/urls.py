from django.urls import path
from .views import *
app_name = 'misi_utama'

urlpatterns = [
    path('read_misi_utama_admin/', read_misi_utama_admin, name='read_misi_utama_admin'),
    path('read_misi_utama_pemain/', read_misi_utama_pemain, name='read_misi_utama_pemain'),
    path('detail_misi/', detail_misi, name='detail_misi'),
    path('create_misi_utama/', create_misi_utama, name='create_misi_utama')
]