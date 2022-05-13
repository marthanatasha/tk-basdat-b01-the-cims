from django.urls import path
from .views import *
app_name = 'menjalankan_misi_utama'

urlpatterns = [
    path('read_menjalankan_misi_utama_admin/', read_menjalankan_misi_utama_admin, name='read_menjalankan_misi_utama_admin'),
    path('read_menjalankan_misi_utama_pemain/', read_menjalankan_misi_utama_pemain, name='read_menjalankan_misi_utama_pemain'),
]